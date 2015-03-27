# Author: Chad Clough
# Created: 3/23/2015
# Last Modified: 3/25/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
import time
import pickle


http = urllib3.PoolManager()

class Recipe:
    def __init__(self, name, author):
        self.name = name.encode('ascii', 'ignore')
        self.author = author.encode('ascii', 'ignore')
        self.attributes = []
        self.ingredients = []

    def __str__(self):
        obj = str(self.name) + " by: " + str(self.author) + "\nattributes: "
        for attribute in self.attributes:
            obj = obj + str(attribute) + ", "
        obj = obj + "\ningredients: "
        for ingredient in self.ingredients:
            obj = obj + str(ingredient) + ", "
        return obj
		
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient.encode('ascii', 'ignore'))

    def add_attribute(self, attribute):
        self.attributes.append(attribute.encode('ascii', 'ignore'))

def get_cookstr_data(url):
    try:
        response = http.request('GET', url)
    except urllib3.exceptions.HTTPError, e:
        print('HTTPError = ' + str(e))
        return 
    except Exception, e:
        print("Error = " + str(e))
        return

    return bs4.BeautifulSoup(response.data)
		
def get_recipe(url):
    """
        Gets a recipe from cookstr

        Args:
            url: The url to the recipe that were scraping

        Returns:	
            A recipe object with the recipe scraped from the url
    """
    chicken_noodle = get_cookstr_data(url)

    #scrape recipe information
    try:
        name = chicken_noodle.findAll('span', {"itemprop" : "name"})[0].text
        author =  chicken_noodle.findAll('span', {"itemprop" : "author"})[0].text
    except Exception, e:
        print("Error = " + str(e))
        return
        
    dish = Recipe(name, author)
    
    attributes = chicken_noodle.findAll('span', {'class' : "attr value"})
    for attribute in attributes:
        dish.add_attribute(attribute.text)

    ingredients = chicken_noodle.findAll('span', {"class" : "ingredient"})
    for ingredient in ingredients:
        dish.add_ingredient(ingredient.text)

    return dish
	
def save_object(obj, path):
    with open(path, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    
def get_recipes(n):
    """
        Gets n recipes from cookstr

        Args:
            n: The number of recipes to scrape
        returns:
            A list of recipes
	"""
    url = 'http://www.cookstr.com/searches/surprise'
    recipe_list = list()
    
    #retrieve the recipes
    for i in range(1, n):
        try:
            dish = get_recipe(url)
            #check for duplicate recipes
            if dish in recipe_list:
                n = n + 1
                continue
            else:
                recipe_list.append(dish)
                time.sleep(0.25) #prevent ddos
        except Exception, e:
            print("Error = " + str(e))
            n = n + 1

    return recipe_list
		
if __name__ == '__main__':
    
    #recipes = get_recipes(1000)
    #save_object(recipes, 'recipes.p')
    
    file = open("recipes.p", 'rb')
    object_file = pickle.load(file)
    for r in object_file:
        print r
        print '\n'
    print len(object_file)