# Author:   Chad Clough
#           github/cclough715
#
# Created:  3/27/2015

from cookstrScraper import Recipe
from collections import Counter
import pickle

def get_ingr_freq(recipeFile, num_most_ing):
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
     
def get_recipes(recipeFile, most_freq_ingr):
    ingr_list = list()
    recipe_list = list()
    
    invalid_ingr = False
    
    for recipe in recipeFile:
        if recipe is not None:
            ingredients = getattr(recipe, 'ingredients')
            for ingredient in ingredients:
                if ingredient not in most_freq_ingr:
                    invalid_ingr = True
            
            if not invalid_ingr:
                recipe_list.append(recipe)
            else:
                invalid_ingr = False
            
    return recipe_list
    

if __name__ == '__main__':
    file = open("asian.p", 'rb')
    object_file = pickle.load(file)
    numIng = 11
    
    most_freq_ingr = get_ingr_freq(object_file, numIng)
    recipe_list = get_recipes(object_file, most_freq_ingr)
    
    for ing in most_freq_ingr:
        print ing
        
    for rec in recipe_list:
        print rec
        print "\n"
        
    print ("Number of ingredients: %d\nNumber of recipes found: %d" % (numIng, len(recipe_list)))
    
    print len(recipe_list)