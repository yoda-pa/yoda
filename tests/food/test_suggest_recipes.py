from mock import patch
import unittest
import yoda
from click.testing import CliRunner

class TestSuggestRecipes(unittest.TestCase):
    """
    Test for the following commands:
        | Module: food
        | command: suggest_recipes
    """
    RANDOM_RECIPE = {
        'meals': [{
            'strMeal': 'Honey Teriyaki Salmon',
            'strInstructions': 'Mix all the ingredients in the Honey Teriyaki Glaze together. Whisk to blend well. Combine the salmon and the Glaze together.\r\n\r\nHeat up a skillet on medium-low heat. Add the oil, Pan-fry the salmon on both sides until it\u2019s completely cooked inside and the glaze thickens.\r\n\r\nGarnish with sesame and serve immediately.',
            'strIngredient1': 'Salmon', 'strIngredient2': 'Olive oil',
            'strIngredient3': 'Soy Sauce',
            'strIngredient4': 'Sake', 'strIngredient5': 'Sesame',
            'strMeasure1': '1 lb', 'strMeasure2': '1 tablespoon',
            'strMeasure3': '2 tablespoons', 'strMeasure4': '2 tablespoons',
            'strMeasure5': '4 tablespoons'
        }]
    }
    

    def __init__(self, methodName="runTest"):
        super(TestSuggestRecipes, self).__init__()
        self.runner = CliRunner()

    @patch('modules.food.requests')
    def runTest(self, requests):
        requests.get.json.return_value = self.RANDOM_RECIPE
        result = self.runner.invoke(yoda.cli, ["food", "suggest_recipes"], input='random')
        self.assertIsNone(result.exception)

        result = self.runner.invoke(yoda.cli, ["food", "suggest_recipes"], input='american')
        self.assertIsNone(result.exception)