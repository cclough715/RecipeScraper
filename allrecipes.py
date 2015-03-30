# Authors:   Chad Clough, Dan Smith
#           github/cclough715
#
# Created:  3/28/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
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
        
        if len(recipe_links) > 0:
            for link in recipe_links:
                #print link
                if link is not None:
                     #ensure we don't count staff picks twice and we're not selecting a collection
                    if('StaffPicks' not in link['id'] and 'browsedeeper' not in link['href']):
                        recipe_url = 'http://www.allrecipes.com' + link.get('href')
                        recipes.append(get_recipe(recipe_url))
                    
            page = page + 1
            url = 'http://allrecipes.com/Recipes/' + category +'/main.aspx?Page=' + str(page)
            soup = recipeScraper.get_soup_data(url)
        else:
            has_recipes = False
    
    return recipes
	
def encode(text):
    return text.encode('ascii', 'ignore')
    