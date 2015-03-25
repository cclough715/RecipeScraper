# Author: Chad Clough
# Created: 3/23/2015
# Last Modified: 3/25/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
import sys
import time

http = urllib3.PoolManager()

class Recipe:
    def __init__(self, name, author):
        self.name = name
        self.author = author
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
        self.ingredients.append(ingredient)

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

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
    soup = get_cookstr_data(url)

    #scrape recipe information
    name = soup.findAll('span', {"itemprop" : "name"})[0].text
    author =  soup.findAll('span', {"itemprop" : "author"})[0].text
    
    dish = Recipe(name, author)
    
    attributes = soup.findAll('span', {'class' : "attr value"})
    for attribute in attributes:
        dish.add_attribute(attribute.text)

    ingredients = soup.findAll('span', {"class" : "ingredient"})
    for ingredient in ingredients:
        dish.add_ingredient(ingredient.text)

    return dish
	
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
    try:
        for i in range(1, n):
            dish = get_recipe(url)
            
            if dish in recipe_list:
                i = i - 1
                continue
            else:
                recipe_list.append(dish)
        time.sleep(0.25) #prevent ddos
    except Exception, e:
        print("Error = " + str(e))

    return recipe_list
		
if __name__ == '__main__':
    recipes = get_recipes(10)
    for r in recipes:
        print r
        print '\n'