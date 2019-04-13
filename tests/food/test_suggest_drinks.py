from mock import patch
import unittest
import yoda
from click.testing import CliRunner


class TestSuggestDrink(unittest.TestCase):
    """
    Test for the following commands:

        | Module: food
        | command: suggest_drinks
    """
    RANDOM_DRINK = {
        'drinks': [{
            'strDrink': 'Oatmeal Cookie',
            'strInstructions': 'Just mix it all together.',
            'strIngredient1': 'Kahlua', 'strIngredient2': 'Bailey',
            'strIngredient3': 'Butterscotch schnapps',
            'strIngredient4': 'Jagermeister', 'strIngredient5': 'Goldschlager',
            'strMeasure1': '2 parts', 'strMeasure2': '2 parts',
            'strMeasure3': '4 parts', 'strMeasure4': '1 part',
            'strMeasure5': '1/2 part'
        }]
    }

    def __init__(self, methodName="runTest"):
        super(TestSuggestDrink, self).__init__()
        self.runner = CliRunner()

    @patch('modules.food.requests')
    def runTest(self, requests):
        requests.get.json.return_value = self.RANDOM_DRINK
        # Test Drink Suggestion
        result = self.runner.invoke(yoda.cli, ["food", "suggest_drinks"])
        self.assertIsNone(result.exception)
