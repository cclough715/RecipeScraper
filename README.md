RecipeScraper
=============

RecipeScraper scrapes recipe information including nutritional information and ingredients from 
[Cookstr](www.cookstr.com) and [AllRecipes](www.allrecipes.com). Recipes scraped [AllRecipes](www.allrecipes.com)
can be exported to a csv format. 

# Installation:
Requires Python 2.7

Dependencies
````
urllib3
beautifulsoup
````

# Usage:
## Scraping from AllRecipes:
This will scrape all recipes within a collection. Look at the url of the website to 
find the collection's name. 

allrecipes.com/recipes/collection-name/
````
> python main.py Main-Dish/Ribs
````
## Output:
````
Scraping allrecipes for 'Main-Dish/Ribs' recipes
This may take a while...

Scraping page: 1...
Scraping page: 2...
...
Scraping page: 210...

Stewed Korean Short Ribs (Kalbi Jim) by: Iggy
attributes: [{'nutrient': 'Calories', 'amount': '647', 'percent': '32%'}, 
{'nutrient': 'Carbohydrates', 'amount': '14.1', 'percent': '5%'}, ... }]
ingredients: beef, shorts ribs, trimmed, green onion, chopped, carrots, peeled and chopped, garlic,
minced, fresh giner root, chopped, reduced-sodium soy sauce, brown sugar, water to cover

...

Number of recipes found: 165
Total scrape time: 0 days, 0 hours, 2 minutes, 56 seconds
````


## Scraping from Cookstr:
This will scrape all Italian recipes found using Cookstr's search engine
````
> python main.py German -c
````

## Output:
````
Scraping cookstr for 'German' recipes
This may take a while...

Scraping Page: 1...
Scraping Page: 2...
...
Scraping Page: 7...

Pot Roast of Beef by: Mimi Sheraton
attributes: Main Course, Half Day, Moderate, 2 Times
ingredients: brisket, salt pork, Salt, Flour, butter, onion, carrot, leek, parsley 
root, celery, bay leaf, pumpernickel, beef stock, sour cream, tomato puree

...

Sourdough Bread with Fennel Seeds by: Victoria Blashford-Snell
attributes: Side Dish, A Day or More, Moderate, Inexpensive, 3 Times
ingredients: bread flour, yeast, water, bread flour, yeast, sugar, fennel seeds, salt, water

Number of recipes found: 60
Total scrape time: 0 days, 0 hours, 0 minutes, 58 seconds
````
