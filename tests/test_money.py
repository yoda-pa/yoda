# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestHealth(TestCase):
    """
        Test for the following commands:

        | Module: health
        | command: health
    """

    def __init__(self, methodName='runTest'):
        super(TestHealth, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['money', 'status'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['money'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['money', 'setup'], input="SGD\n200")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['money', 'exp'], input='Spent 20 dollars on a t-shirt')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['money', 'exps'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['money', 'exps_year'])
        self.assertEqual(result.exit_code, 0)
