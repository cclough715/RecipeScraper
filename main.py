import argparse
import recipeScraper
import allrecipes
import cookstr
from datetime import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrapes recipes from cookstr and allrecipes.')
    parser.add_argument('--cookstr', '-c',
        action  = 'store_true',
        help    = 'scrapes cookstr instead of allrecipes')
        
    parser.add_argument('query',
        type = str)
        
    args = parser.parse_args()
    query = args.query
    
    
    if args.cookstr:
        site = 'cookstr'
    else:
        site = 'allrecipes'
    
    print ("Scraping %s for '%s' recipes\nThis may take a while...\n" % (site, query))
    
    start   = datetime.now()
    if args.cookstr:
        recipes = cookstr.get_recipes(query)
    else:
        recipes = allrecipes.get_recipes(query)
    end     = datetime.now()
    elapsed = end - start #calculate total scrape time
    
    #save our recipes to a file
    file_name = args.query.replace('/', '_')
    recipeScraper.save_object(recipes, file_name + '.p')
    
    #read back the recipes we just scraped
    savedRecipes = recipeScraper.get_object(file_name + '.p')
    for r in savedRecipes:
        print r
        print '\n'

    print ("\nNumber of recipes found: %d" % (len(savedRecipes)))

    #display total scrape time
    days    = divmod(elapsed.total_seconds(), 86400)
    hours   = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = minutes[1]
    print ("Total scrape time: %d days, %d hours, %d minutes, %d seconds" % 
        (days[0], hours[0], minutes[0], seconds))
