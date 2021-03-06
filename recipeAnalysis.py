# Author:   Chad Clough
#           github/cclough715
#
# Created:  3/27/2015

import argparse
import recipeScraper
import allrecipes
from recipeScraper import Recipe
from collections import Counter
import csv

allrecipes_stop_words = set(['or', 'as', 'needed', 'fresh', 'to', 'taste', 
    ', ', 'chopped', 'grated', 'minced', 'shredded', 'all-purpose', 
    'ground', 'dried', 'and', 'skinless', 'boneless', 'halves', 'active',
    'dry'])

def get_ingr_freq(recipeFile, num_most_ing):
    ''' Finds the most frequent ingredients in file with a list of Recipes
        
        Args:
            recipeFile: A serialized list of Recipes
            num_most_ing: The number of frequent ingredients we're looking for
        
        Returns:
            A dictionary with [num_most_ing] ingredients and the percentage of
                recipes that ingredient is found in
    '''
    ingr_list = list()
    
    for recipe in recipeFile:
        if recipe is not None:
            ingredients = getattr(recipe, 'ingredients')
            for ingredient in ingredients:
                ingr_list.append(ingredient.lower())
    
    num_ing = len(ingr_list)
    counts = Counter(ingr for ingr in ingr_list)
    keyingr = {a: b for a, b in counts.most_common(num_most_ing)}
    
    for key in keyingr:
        keyingr[key] = keyingr[key] / float(num_ing)
           
    return keyingr
     
def get_recipes(recipeFile, inventory):
    ''' Gets a list of recipes that only use ingredients in our inventory
    
        Args:
            recipeFile: a serialized list of all of the recipes we're going to 
                use
            inventory: a list of all the ingredients we can use to make our 
                recipes
        
        Returns:
            list; A list of recipes that only use ingredients in our inventory
    '''
    ingr_list = list()
    recipe_list = list()
    
    invalid_ingr = False
    
    for recipe in recipeFile:
        if recipe is not None:
            ingredients = getattr(recipe, 'ingredients')
            for ingredient in ingredients:
                if ingredient not in inventory:
                    invalid_ingr = True
            
            if not invalid_ingr:
                recipe_list.append(recipe)
            else:
                invalid_ingr = False
            
    return recipe_list
  
  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyses recipe lists to ' \
    'find the most common ingredients and finds recipes that use only' \
    'those ingredients')
        
    parser.add_argument('--cookstr', '-c',
        action  = 'store_true',
        help    = 'scrapes cookstr instead of allrecipes')
        
    parser.add_argument('--csv',
        action  = 'store_true',
        help    = 'converts a pickle file into a csv file')

    parser.add_argument('filepath', type=str)
    args = parser.parse_args()
    path = args.filepath
    
    object_file = recipeScraper.get_object(path + '.p')
    
    if not args.csv:
        numIng = 40 #we're going to use the 40 most common found ingredients
        
        most_freq_ingr = get_ingr_freq(object_file, numIng)
        recipe_list = get_recipes(object_file, most_freq_ingr)
        
        for ing in most_freq_ingr:
            print ing
            
        for rec in recipe_list:
            print rec
            print "\n"
            
        print 'Number of ingredients: {}\nNumber of recipes found: {}'.format(
            numIng, len(recipe_list))
    else:
        savedRecipes = recipeScraper.get_object(args.filepath + '.p')
        allrecipes.export_csv(savedRecipes, args.filepath + '.csv')
        
        