import random
import sys
import pprint

if sys.version_info[0] >= 3:
    from urllib.parse import quote
else:
    from urllib import quote

import click
import requests

API_KEY = 'PssDzQz9vE51CseZKIKtUc76g-nFf5Xmv-Ha0_SGBowyEME0YNxG9iGMDsQ722rAPHLLupyUlMWHRdqaCCnrp-RAFLGVYIWfOAuB2Wn-5C0aR-1bnA5Csu4PGDCMXHYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'


@click.group()
def food():
    """
    Food module... yum
    Suggest recipes for food, drinks, and restaurants
    """

@food.command()
def suggest_drinks():
    """
    Get suggested a random drink recipe from the Cocktail DB API.
    """
    drinkURL = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
    randomDrinkURL = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    drinkIngredients = []

    def getDrinkSuggestion():
        req = requests.get(randomDrinkURL)
        parsed_response = req.json()
        drinkInfoJSON = parsed_response["drinks"]
        drink = drinkInfoJSON[0]["strDrink"]

        click.echo("Like you need a drink you look.  Hmmmmmm.")
        click.echo("---------------------" + drink + "---------------------")
        getIngredients(drink)
        getDrinkInstructions(drink)

    def getDrinkInstructions(drink):
        req = requests.get(drinkURL + drink)
        parsed_response = req.json()
        drinkInfoJSON = parsed_response["drinks"]
        drinkInstructions = drinkInfoJSON[0]["strInstructions"]
        click.echo("Instructions: " + drinkInstructions)

    def getIngredients(drink):
        req = requests.get(drinkURL + drink)
        parsed_response = req.json()
        drinkInfoJSON = parsed_response["drinks"]
        click.echo("Ingredients: ")
        for ingNumber in range(1, 16):
            ingredient = drinkInfoJSON[0]["strIngredient" + str(ingNumber)]
            qty = drinkInfoJSON[0]["strMeasure" + str(ingNumber)]
            if ingredient:
                if not qty:
                    output_str = "{} (as needed)".format(ingredient)
                else:
                    output_str = "{} x {}".format(ingredient, qty)

                click.echo(output_str)
                drinkIngredients.append(ingredient)

    getDrinkSuggestion()


@food.command()
def suggest_restaurant():
    """
    Get a suggested restaurant in your city.
    """
    if sys.version_info[0] >= 3:
        city = input('What city are you in? ')
        cuisine = input('What type of food are you interested in? ')
    else:
        city = raw_input('What city are you in? ')
        cuisine = raw_input('What type of food are you interested in? ')
    yelp_url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    url_params = {
        'term': 'restaurant+' + cuisine,
        'categories': cuisine,
        'location': city.replace(' ', '+'),
        'limit': 50
    }
    req = requests.get(yelp_url, headers={'Authorization': 'Bearer ' + API_KEY}, params=url_params)
    parsed_response = req.json()
    businesses = parsed_response['businesses']
    if len(businesses) == 0:
        click.echo('Could not find any restaurants like that in your city :(')
    else:
        restaurant = random.choice(businesses)
        click.echo()
        click.echo("Why don't you try THIS restaurant tonight!")
        click.echo()
        click.echo(restaurant['name'] + ' on ' + restaurant['location']['address1'])
        click.echo('Book a table at ' + restaurant['phone'])


@food.command()
def suggest_recipes():
    """
    Get suggested a random meal recipe from theMealDB API.
    """
    click.echo("Categories: American, British, Canadian, Chinese, Dutch, Egyptian, " + 
        "French, Greek, Indian, Irish, Italian, Jamaican, Japanese, Kenyan, Malaysian, Mexican, " + 
        "Moroccan, Russian, Spanish, Thai, Unknown, Vietnamese whoe hasldf")
    click.echo()

    if sys.version_info[0] >= 3:
        category = input('Choose a category above or type \'Random\' for a random recipe suggestion: ')
    else:
        category = raw_input('Choose a category above or type \'Random\' for a random recipe suggestion: ')

    category = category.capitalize()
    
    def outputMeal(mealJSON):
        click.echo()
        click.echo("---------------------" + mealJSON[0]["strMeal"] + "---------------------")
        click.echo()

        #print ingredients
        click.echo("Ingredients: ")
        for i in range(1, 25):
            ingredient = mealJSON[0]["strIngredient" + str(i)]
            qty = mealJSON[0]["strMeasure" + str(i)]
            if ingredient:
                ingredientStr = ingredient.encode("utf-8")
                if not qty:
                    output_str = "{} (as needed)".format(ingredientStr)
                else:
                    qtyStr = qty.encode("utf-8")
                    output_str = "{} x {}" .format(ingredientStr, qtyStr)

                click.echo(output_str)
            else:
                break

        #print instructions
        click.echo()
        click.echo("Instructions: " + mealJSON[0]["strInstructions"])

    def randomURL():
        #fetch random meal from database
        randomURL = "https://www.themealdb.com/api/json/v1/1/random.php"

        req = requests.get(randomURL)
        parsed_response = req.json()

        outputMeal(parsed_response["meals"])
        return parsed_response["meals"]

    def categoryURL(category):
        #fetch random meal from a specific category
        categoryURL = "https://www.themealdb.com/api/json/v1/1/filter.php?a=" + category

        req = requests.get(categoryURL)
        parsed_response = req.json()

        #if the category is invalid, the result we get is 'None'
        if(parsed_response["meals"] == None):
            click.echo()
            click.echo("Invalid Input")
            click.echo()
            exit(1)

        
        #len(parsed_response["meals"]) is number of meals in that category
        #get a random one
        length = len(parsed_response["meals"]) - 1
        rand = random.randint(0, 10)
        if rand  + 1 > length:
            rand = length
        mealID = parsed_response["meals"][rand]["idMeal"]
        
        mealURL = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + mealID
        req = requests.get(mealURL)
        parsed_response = req.json()

        outputMeal(parsed_response["meals"])

    if category == "Random":
        data = randomURL()
    else:
        data = categoryURL(category)