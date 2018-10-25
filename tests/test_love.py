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
        result = self.runner.invoke(yoda.cli, ["love"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "status"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "setup"], input="A\nD\nF")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "notes"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "note"], input="la la la...\n")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "note"], input="la la la...\n")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "notes"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "status"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["love", "invalid_argument"])
        self.assertEqual(result.exit_code, 0)
