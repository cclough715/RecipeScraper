# Author:   Chad Clough
#           github/cclough715
#
# Created:  3/28/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pickle

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

        

def get_soup_data(url):
    ''' Gets the contents of a url in the form of a BeautifulSoup object 
    
        Args:
            url: the url we're trying to scrape
            
        Returns:
            BeautifulSoup; a bs4 object with the contents of url
    '''
    try:
        response = http.request('GET', url)
    except urllib3.exceptions.HTTPError, e:
        print('HTTPError = ' + str(e))
        return 
    except Exception, e:
        print("Error = " + str(e))
        return

    return bs4.BeautifulSoup(response.data)
		
        
def save_object(obj, path):
    ''' Serialzes an object and saves it into a file
    
        Args:
            obj: The object to be serialized
            path: The filepath of where we want to save the object
    '''
    with open(path, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
def get_object(path):
    file = open(path, 'rb')
    return pickle.load(file)