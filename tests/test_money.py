# coding=utf-8
from mock import patch
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestHealth(TestCase):
    """
        Test for the following commands:

        | Module: health
        | command: health
    """

    def __init__(self, methodName="runTest"):
        super(TestHealth, self).__init__()
        self.runner = CliRunner()

    @patch('modules.money.convert')
    @patch('modules.money.currency_codes')
    @patch('modules.money.currency_rates.get_rates')
    def runTest(self, get_rates, currency_codes, convert):
        currency_codes.get_symbol.return_value = 'USD'
        get_rates.return_value = {'USD': 1}
        convert.return_value = 1
        currency_codes.get_currency_name.return_value = 'USD'

        result = self.runner.invoke(yoda.cli, ["money", "status"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["money"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["money", "setup"], input="SGD\n200")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            yoda.cli, ["money", "exp"], input="Spent 20 dollars on a t-shirt"
        )
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["money", "exps"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["money", "exps_months"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            yoda.cli, ["money", "convert"], input="INR USD\n100"
        )
        self.assertEqual(result.exit_code, 0)
