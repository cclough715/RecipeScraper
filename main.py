import argparse
import recipeScraper
import allrecipes
import cookstr
from datetime import datetime
import time

def scrape_recipes(site):
    print "Scraping {0} for '{1}' recipes\nThis may take a while...\n".format(site, query)
  
    if site == 'cookstr':
        return cookstr.get_recipes(query)
    else:
        return allrecipes.get_recipes(query)
        
def print_scrape_time(time):
    #display total scrape time
    days    = divmod(time, 86400)
    hours   = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = minutes[1]
    
    s = '''Total scrape time: {0:.0f} days, {1:.0f} hours, {2:.0f} minutes, 
     {3:.0f} seconds'''
    
    print s.format(days[0], hours[0], minutes[0], seconds)

if __name__ == '__main__':
    #create parser
    parser = argparse.ArgumentParser(description =
        'Scrapes recipes from cookstr and allrecipes.')
    parser.add_argument('--cookstr', '-c', action  = 'store_true',
        help    = 'scrapes cookstr instead of allrecipes')
    parser.add_argument('--noscrape', '-ns', action  = 'store_true')     
    parser.add_argument('query',
        type = str)
    args = parser.parse_args()
    
    #get arguments
    query = args.query
    if args.cookstr:
        site = 'cookstr'
    else:
        site = 'allrecipes'
    
    if not args.noscrape:
        start   = time.clock()#datetime.now()
        recipes = scrape_recipes(site)
        #end     = time.clock()#datetime.now()
        elapsed = (time.clock() - start) #calculate total scrape time
    
        #save our recipes to a file
        file_name = args.query.replace('/', '_')
        recipeScraper.save_object(recipes, file_name + '.p')
        
    file_name = args.query.replace('/', '_')
    #read back the recipes we just scraped
    savedRecipes = recipeScraper.get_object(file_name + '.p')
    for r in savedRecipes:
        print '{0}\n'.format(str(r))

    print '\nNumber of recipes found: {0}'.format(len(savedRecipes))

    if not args.noscrape:
        print_scrape_time(elapsed)

