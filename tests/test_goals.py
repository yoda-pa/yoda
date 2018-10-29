# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestGoals(TestCase):
    """
        Test for the following commands:

        Assumes empty goals list.

        | Module: goals
        | command: goals new, view, tasks, complete, analyze
    """

    def __init__(self, methodName="runTest"):
        super(TestGoals, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["goals"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["goals", "view"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            yoda.cli, ["goals", "new"], input="test\ntest goal\n2020-02-02"
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["goals", "view"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["goals", "tasks"], input="test")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["goals", "complete"], input="1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["goals", "analyze"])
        self.assertEqual(result.exit_code, 0)
