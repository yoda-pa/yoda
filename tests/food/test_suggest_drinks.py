import unittest
import yoda
from click.testing import CliRunner


class TestSuggestDrink(unittest.TestCase):
    """
    Test for the following commands:

        | Module: food
        | command: suggest_drinks
    """
    def __init__(self, methodName='runTest'):
        super(TestSuggestDrink, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        #Test Drink Suggestion
        result = self.runner.invoke(yoda.cli, ['food', 'suggest_drinks'])
        self.assertIsNone(result.exception)