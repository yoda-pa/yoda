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

    def __init__(self, methodName="runTest"):
        super(TestPeople, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["people"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["people", "status"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'setup'], input="test people\n09876543\n1994-01-19\n1122334455")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["people", "status"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'note'], input='test people\ntest note\n-')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            yoda.cli, ["people", "like"], input="test people\ntest like\n-"
        )
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["people", "likes"], input="test people")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["people", "notes"], input="test people")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'likes'], input='test people1')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["people", "notes"], input="test people1")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["people", "invalid_argument"])
        self.assertEqual(result.exit_code, 0)

        # negative tests
        result = self.runner.invoke(yoda.cli, ['people', 'notes'], input='invalid')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'likes'], input='invalid')
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['people', 'like'], input='invalid')
        self.assertEqual(result.exit_code, 0)
