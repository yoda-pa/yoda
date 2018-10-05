# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestPeople(TestCase):
    """
        Test for the following commands:

        | Module: People
        | command: people
    """

    def __init__(self, methodName='runTest'):
        super(TestPeople, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['people'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'status'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'setup'], input="A\nD\nF")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'notes'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'note'], input='la la la...\n')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'note'], input='la la la...\n')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'notes'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'status'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'invalid_argument'])
        self.assertEqual(result.exit_code, 0)
