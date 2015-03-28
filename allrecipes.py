# Author:   Chad Clough
#           github/cclough715
#
# Created:  3/28/2015

import urllib3
import bs4
from bs4 import BeautifulSoup
import time
from datetime import datetime
import cookstrScraper

def get_recipe(url):
    ''' Gets a recipe from cookstr

        Args:
            url: The url to the recipe that were scraping

        Returns:	
            A recipe object with the recipe scraped from the url
    '''
    
    soup = cookstrScraper.get_data(url)

    #scrape recipe information
    try:
        name = soup.findAll('h1', {"id" : "itemTitle"})[0].text
        author =  soup.findAll('span', {"class" : "author"}).descendants[0].text
    except Exception, e:
        print("Error = " + str(e))
        return
        
    dish = Recipe(name, author)
    
    #attributes = soup.findAll('span', {'class' : "attr value"})
    #for attribute in attributes:
    #    dish.add_attribute(attribute.text)
    dish.add_attribute('not yet implemented')
    
    ingredients = soup.findAll('span', {"class" : "ingredient-name"})
    for ingredient in ingredients:
        dish.add_ingredient(ingredient.text)

    return dish
	


<h1 id="itemTitle" class="plaincharacterwrap fn" itemprop="name">Salisbury Steak with Mushrooms</h1>
<a id="lnkUser1087335" href="http://allrecipes.com/cook/18759336/profile.aspx">ESKARINA</a>
<span id="lblSubmitter" class="author" rel="nofollow" itemprop="author"><a id="lnkUser920855" href="http://allrecipes.com/cook/1407566/profile.aspx">CHRCAMILLO</a></span>
<span id="lblIngName" class="ingredient-name">beef broth</span>


<div class="rating-stars-img" title="Most cooks definitely will make this recipe again">
					<meta itemprop="ratingValue" content="4.243902">
				</div>

<span id="totalMinsSpan"><em class="emp-orange">40</em> mins</span>

<div id="nutritionSummary" class="nutrSumWrap">

        <h3>Nutrition</h3>

        
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Calories</li>
                    <li class="units"><span id="lblNutrientValue">323</span> kcal</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:16%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">16%</li>
                </ul>     
            
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Carbohydrates</li>
                    <li class="units"><span id="lblNutrientValue">17.2</span> g</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:6%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">6%</li>
                </ul>     
            
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Cholesterol</li>
                    <li class="units"><span id="lblNutrientValue">121</span> mg</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:40%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">40%</li>
                </ul>     
            
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Fat</li>
                    <li class="units"><span id="lblNutrientValue">15.8</span> g</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:24%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">24%</li>
                </ul>     
            
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Fiber</li>
                    <li class="units"><span id="lblNutrientValue">1.5</span> g</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:6%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">6%</li>
                </ul>     
            
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Protein</li>
                    <li class="units"><span id="lblNutrientValue">26.6</span> g</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:53%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">53%</li>
                </ul>     
            
                <ul id="ulNutrient" class="nutrSumList">
                    <li class="categories">Sodium</li>
                    <li class="units"><span id="lblNutrientValue">1129</span> mg</li>
                    <li class="nutrition-rating">
                        <ul>
                            <li id="divNutrientGradient" class="nutrition-rating-grad" style="width:45%"></li>
                            <li class="nutrition-rating-img"></li>
                        </ul>
                    </li>
                    <li class="percentages">45%</li>
                </ul>     
    </div>