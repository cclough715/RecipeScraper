# Author: Chad Clough
# Created: 3/23/2015
# Last Modified: 3/24/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
import sys

http = urllib3.PoolManager()

def get_recipe(url):
	"""Gets a recipe from cookstr
	
		Args:
			url: The url to the recipe that were scraping
	
		returns:
			
	"""
	try:
		response = http.request('GET', url)
	except urllib3.exceptions.HTTPError, e:
		print('HTTPError = ' + str(e))
		return
	except Exception, e:
		print("Error = " + str(e))
		return
		
	soup = bs4.BeautifulSoup(response.data)
	
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
	
def get_recipes(n):
	"""Gets n recipes from cookstr
	
		Args:
			n: The number of recipes to scrape
			
		returns:
			A list of recipes
	"""
	next = soup.findAll('img', {"alt" : "Surprise-me-button-transp"})
	
	
	if len(content) == 0:
		print "Error: No content found. url = " + url
	
	#retrieve the recipes
	#for i in range(1, n):
		#get name
		#check to see if we already have this recipe
			#if so then i-- and continue
		#scrape elements then add to list
		
	return list
		
if __name__ == '__main__':
	print get_recipe('http://www.cookstr.com/recipes/pickled-carrot-sticks')