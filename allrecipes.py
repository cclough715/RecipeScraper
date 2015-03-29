# Authors:   Chad Clough, Dan Smith
#           github/cclough715
#
# Created:  3/28/2015

import argparse
import urllib3
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import recipeScraper

def get_recipe(url):
    ''' Gets a recipe from allrecipes
        Args:
            url: The url to the recipe that were scraping
        Returns:	
            A recipe object with the recipe scraped from the url
    '''
    
    soup = recipeScraper.get_soup_data(url)

    #scrape recipe information
    try:
        name = soup.findAll('h1', {"id" : "itemTitle"})[0].text
    except IndexError:
        print ("\tError: Recipe name not found")
        name = 'N/A'
    try:   
        author =  soup.find('span', {"class" : "author"}).text
    except IndexError:
        print ("\tError: Author not found")
        author = 'N/A'
        
    dish = recipeScraper.Recipe(encode(name), encode(author))
    
    nutrition = soup.findAll('ul', {'id' : 'ulNutrient'})
    nutrition_info = []
    for nutrient in nutrition:
        nutrient_info = {}
        nutrient_info['nutrient'] = encode(nutrient.find('li', {'class' : 'categories'}).text)
        nutrient_info['amount'] = encode(nutrient.find('span', {'id' : 'lblNutrientValue'}).text)
        nutrient_info['percent'] = encode(nutrient.find('li', {'class' : 'percentages'}).text)
        nutrition_info.append(nutrient_info)
    
    dish.add_attribute(nutrition_info)
    
    ingredients = soup.findAll('span', {"class" : "ingredient-name"})
    for ingredient in ingredients:
        dish.add_ingredient(encode(ingredient.text))

    return dish
    
def get_recipes(category):
    ''' Gets a list of all recipes found in a specific category
        
        Args:
            category: A search term for a type of recipe (ex. 'italian', 'asian', etc.)
            
        Returns:
            A list of all recipes found within the category
    '''
    recipes = list()
    page = 1
    url = 'http://www.allrecipes.com/Recipes/' +category
    soup = recipeScraper.get_soup_data(url)
    has_recipes = True

    while has_recipes:
        print ("Scraping page: %d..." % (page))
        #grab each recipe on this search page
        recipe_links = soup.findAll('a', {"class" : "title"})
        
        #BUG: check to make sure class is not 'coll-info' this currently 
        #grabs collections and treats them as recipes
        
        #BUG: check to see if the id contains 'StaffPicks' these recipes
        #are currently being counted twice
        if len(recipe_links) > 0:
            for link in recipe_links:
                if link is not None:
                    recipe_url = 'http://www.allrecipes.com' + link.get('href')
                    print recipe_url
                    recipes.append(get_recipe(recipe_url))
            page = page + 1
            url = 'http://allrecipes.com/Recipes/' +category +'/main.aspx?Page=' + str(page)
            soup = recipeScraper.get_soup_data(url)
        else:
            has_recipes = False
    
    return recipes
	
def encode(text):
    return text.encode('ascii', 'ignore')
    
if __name__ == '__main__':
    #TODO: Add a parser 
    category = "appetizers-and-snacks"
    print ("Scraping allrecipes for category: '%s' \nThis may take a while...\n" % (category))
    
    start   = datetime.now()
    recipes = get_recipes(category)
    end     = datetime.now()
    elapsed = end - start #calculate total scrape time
    
    #save our recipes to a file
    file_name = category.replace('/', '_')
    recipeScraper.save_object(recipes, file_name + '.p')
    
    #read back the recipes we just scraped
    savedRecipes = recipeScraper.get_object(file_name + '.p')
    for r in savedRecipes:
        print r
        print '\n'

    print ("Number of recipes found: %d" % (len(savedRecipes)))

    #display total scrape time
    days    = divmod(elapsed.total_seconds(), 86400)
    hours   = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = minutes[1]
    print ("Total scrape time: %d days, %d hours, %d minutes, %d seconds" % 
        (days[0], hours[0], minutes[0], seconds))
    