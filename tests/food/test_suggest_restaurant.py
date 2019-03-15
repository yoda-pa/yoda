import unittest

from click.testing import CliRunner

import yoda


class TestSuggestRestaurant(unittest.TestCase):
    """
    Test for the following commands:

        | Module: food
        | command: suggest_restaurant
    """

    def __init__(self, methodName="runTest"):
        super(TestSuggestRestaurant, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # Test Restaurant Suggestion
        result = self.runner.invoke(yoda.cli, ['food', 'suggest_restaurant'], input='Berlin\nJamaican')
        self.assertIn("Why don't you try THIS restaurant tonight!", result.output)
        self.assertIsNone(result.exception)
