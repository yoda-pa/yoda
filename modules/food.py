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
        parsed_response = json.loads(req.content)
        drinkInfoJSON = parsed_response['drinks']
        drink = drinkInfoJSON[0]['strDrink']
        click.echo(drink)
        cont = input('Would you like to try a ' + drink + '?')
        if cont in ['y', 'yes', 'sure', 'ok', 'please', 'yes please']:
            getIngredients(drink)
            getDrinkInstructions(drink)
        else:
            click.echo('Maybe some other time')

    def getDrinkInstructions(drink):
        req = requests.get(drinkURL + drink)
        parsed_response = json.loads(req.content)
        drinkInfoJSON = parsed_response['drinks']
        drinkInstructions = drinkInfoJSON[0]['strInstructions']
        click.echo('Instructions: ' + drinkInstructions)

    def getIngredients(drink):
        req = requests.get(drinkURL + drink)
        parsed_response = json.loads(req.content)
        drinkInfoJSON = parsed_response['drinks']
        click.echo('Ingredients: ')
        for ingNumber in range(1, 16):
            ingredient = drinkInfoJSON[0]['strIngredient' + str(ingNumber)]
            if ingredient != "":
                click.echo(ingredient)
                drinkIngredients.append(ingredient)

    getDrinkSuggestion()