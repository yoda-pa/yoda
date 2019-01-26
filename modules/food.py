import click
import requests

FOOD_URL = 'https://www.themealdb.com/api/json/v1/1/search.php?s='
RANDOM_FOOD_URL = 'https://www.themealdb.com/api/json/v1/1/random.php'
INGREDIENTS = []


def food_request(food):
    req = requests.get(FOOD_URL + food)
    parsed_response = req.json()
    food_json = parsed_response['meals']
    return food_json


def get_meal_instructions(meal):
    click.echo(food_request(meal)[0]['strInstructions'])


def get_ingridients(meal):
    for ingNumber in range(1, 20):
        ingredient = food_request(meal)[0]['strIngredient' + str(ingNumber)]
        qty = food_request(meal)[0]['strMeasure' + str(ingNumber)]
        if ingredient:
            if not qty:
                output_str = "{} (as needed)".format(ingredient)
            else:
                output_str = "{} x {}".format(ingredient, qty)
            click.echo(output_str)
            INGREDIENTS.append(output_str)


@click.group()
def food():
    """
            Food module... yum
            Suggest recipes for food, drinks, and restaurants
    """


@food.command()
def suggest_food():
    """
    Suggests a random meal from the meal DB
    """

    def get_meal_suggestion():
        req = requests.get(RANDOM_FOOD_URL)
        parsed_response = req.json()
        food_json = parsed_response['meals']
        meal = food_json[0]['strMeal']

        click.echo('Try this amazing ' + meal + ', it\'s delicious!')
        click.echo("You will need following :")
        click.echo('------------')
        get_ingridients(meal)
        click.echo('------Follow the instructions below------ :')
        get_meal_instructions(meal)
        click.echo('Bon appetit ! =) ')

    get_meal_suggestion()


@food.command()
@click.argument('meal')
def food_select(meal):
    """
    Displays recipe with measurements and instructions for selected meal preparation
    """

    def chosen_food(meal):
        click.echo('-----Here are ingridients for your {0}!-----'.format(meal))
        get_ingridients(meal)
        click.echo('-----And here are the instructions for {0}-----'.format(meal))
        get_meal_instructions(meal)

    chosen_food(meal)


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
