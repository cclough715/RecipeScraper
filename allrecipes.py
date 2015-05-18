# Authors:   Chad Clough, Dan Smith
#           github/cclough715
#
# Created:  3/28/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
import recipeScraper
import csv

def export_csv(recipes, filename):
    #attribute indexes
    nutrition_info = 0
    calories = 0
    carbs = 1
    cholesterol = 2
    fat = 3
    fiber = 4
    protein = 5
    sodium = 6
    
    name = ''
    file = open(filename, 'wb')
    try:
        writer = csv.writer(file)
        #create header
        writer.writerow(('Name', 'Calories', 'Carbohydrates', 
                         'Cholesterol-Free', 'Fat', 
                         'Fiber', 'Protein', 'Sodium'))
                         
        for recipe in recipes:
            #collect nutritional information
            cal_perc = strip_percent(recipe.attributes[nutrition_info][calories])
            fat_perc = strip_percent(recipe.attributes[nutrition_info][fat])
            car_perc = strip_percent(recipe.attributes[nutrition_info][carbs])
            fib_perc = strip_percent(recipe.attributes[nutrition_info][fiber])
            pro_perc = strip_percent(recipe.attributes[nutrition_info][protein])
            sod_perc = strip_percent(recipe.attributes[nutrition_info][sodium])
            
            try:
                row = (
                    getattr(recipe, 'name'), cal_perc, car_perc,
                    recipe.attributes[nutrition_info][cholesterol]['amount'] == '0', 
                    fat_perc, fib_perc, pro_perc, sod_perc
                )
            except: 
                continue #skip over invalid data
               
            writer.writerow(row)
    except:
        print name 
    finally:
        file.close()
        
def strip_percent(attribute):
    if '<' in attribute:
        return '0'
    else:
        return float(attribute['percent'].strip('%'))
        
def import_csv(filename):
    #TODO: implement
    return recipe

def get_recipe(url):
    ''' Gets a recipe from allrecipes
        Args:
            url: The url to the recipe that were scraping
        Returns:	
            A recipe object with the recipe scraped from the url
    '''
    
    soup = recipeScraper.get_soup_data(url)

    #scrape recipe name and author
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
    
    #create the recipe
    dish = recipeScraper.Recipe(encode(name), encode(author))
    
    #scrape nutritional information
    nutrition = soup.findAll('ul', {'id' : 'ulNutrient'})
    nutrition_info = []
    for nutrient in nutrition:
        nutrient_info = {
            'nutrient' : encode(nutrient.find('li', {'class' : 'categories'}).text),
            'amount'   : encode(nutrient.find('span', {'id' : 'lblNutrientValue'}).text),
            'percent'  : encode(nutrient.find('li', {'class' : 'percentages'}).text)
        }
        nutrition_info.append(nutrient_info)
    dish.add_attribute(nutrition_info)
    if len(nutrition_info) == 0:
        print "\tError: No nutritional information is available for reci" \
        "pe: {} by {}".format(name, author)
        
    #gather ingredient list for recipe
    ingredients = soup.findAll('span', {"class" : "ingredient-name"})
    for ingredient in ingredients:
        dish.add_ingredient(encode(ingredient.text))
    if len(ingredients) == 0:
        print "\tError: No ingredients found. Something is wrong here..." \
        "\nrecipe: {} by {}".format(name, author)

    return dish
    
def get_recipes(category):
    ''' Gets a list of all recipes found in a specific category
        
        Args:
            category: A search term for a type of recipe (ex. 'italian', 
                'asian', etc.)
            
        Returns:
            A list of all recipes found within the category
    '''
    recipes = list()
    page = 1
    url = 'http://www.allrecipes.com/Recipes/' + category
    soup = recipeScraper.get_soup_data(url)
    has_recipes = True            #check if there are any recipes on the page
    only_collections_left = False #check if there is only collections left

    while has_recipes:
        print ("Scraping page: %d..." % (page))
        #grab each recipe on this search page
        recipe_links = soup.findAll('a', {"class" : "title"})
        
        if len(recipe_links) > 0:
            only_collections_left = True
            #scrape each recipe on this page
            for link in recipe_links:
                if link is not None:
                     #ensure we don't count staff picks twice
                    if('StaffPicks' not in link['id'] and    
                        'browsedeeper' not in link['href']): #not a collection
                        
                        r_url = 'http://www.allrecipes.com' + link.get('href')
                        recipes.append(get_recipe(r_url))
                        only_collections_left = False
            #get next page
            page = page + 1
            url =  'http://allrecipes.com/Recipes/' + category
            url += '/main.aspx?Page=' + str(page)
            soup = recipeScraper.get_soup_data(url)
        else:
            has_recipes = False
        
        if only_collections_left:
            has_recipes = False
    
    return recipes
	
def encode(text):
    return text.encode('ascii', 'ignore')
    