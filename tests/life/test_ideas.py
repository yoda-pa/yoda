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

    def __init__(self, methodName="runTest"):
        super(TestHealth, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["ideas", "status"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["ideas", "show"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["ideas", "remove"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["ideas", "add"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["ideas", "remove"])
        self.assertEqual(result.exit_code, 0)
