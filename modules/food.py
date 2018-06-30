import requests
import click
import json

@click.group()
def food():
    """
            Food module... yum
            Suggest recipes for food, drinks, and restaurants
    """

@food.command()
def suggest_drinks():
    drinkURL = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s='
    randomDrinkURL = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
    drinkIngredients = []

    def getDrinkSuggestion():
        req = requests.get(randomDrinkURL)
        parsed_response = req.json()
        drinkInfoJSON = parsed_response['drinks']
        drink = drinkInfoJSON[0]['strDrink']

        click.echo('Like you need a drink you look.  Hmmmmmm.')
        click.echo('---------------------' + drink + '---------------------')
        getIngredients(drink)
        getDrinkInstructions(drink)

    def getDrinkInstructions(drink):
        req = requests.get(drinkURL + drink)
        parsed_response = req.json()
        drinkInfoJSON = parsed_response['drinks']
        drinkInstructions = drinkInfoJSON[0]['strInstructions']
        click.echo('Instructions: ' + drinkInstructions)

    def getIngredients(drink):
        req = requests.get(drinkURL + drink)
        parsed_response = req.json()
        drinkInfoJSON = parsed_response['drinks']
        click.echo('Ingredients: ')
        for ingNumber in range(1, 16):
            ingredient = drinkInfoJSON[0]['strIngredient' + str(ingNumber)]
            qty = drinkInfoJSON[0]['strMeasure' + str(ingNumber)]
            if ingredient != "":
                click.echo(ingredient + ' x ' + qty)
                drinkIngredients.append(ingredient)

    getDrinkSuggestion()