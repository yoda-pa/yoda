# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestDiary(TestCase):
    """
        Test for the following commands:
        
        Assumes empty diary.

        | Module: diary
        | command: diary tasks, nt, ct
    """

    def __init__(self, methodName="runTest"):
        super(TestDiary, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["diary"])
        self.assertEqual(result.exit_code, 0)

        # tasks
        result = self.runner.invoke(yoda.cli, ["diary", "tasks"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "ct"], input="2")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "nt"], input="test task\n-")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "ct"], input="1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "nt"], input="test task 2\n-")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "ct"], input="2")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "ct"], input="3")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            yoda.cli, ["diary", "ut"], input="1\n1\nUpdated Tasks"
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "dct"], input="c")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "dt"], input="1\n1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "tasks"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "analyze"])
        self.assertEqual(result.exit_code, 0)

        # notes
        result = self.runner.invoke(yoda.cli, ["diary", "notes"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            yoda.cli, ["diary", "nn"], input="test note\ntest note1"
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            yoda.cli, ["diary", "nn"], input="test note\ntest note2"
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "dn"], input="1\n1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            yoda.cli, ["diary", "un"], input="1\n1\nupdated task"
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ["diary", "notes"])
        self.assertEqual(result.exit_code, 0)
