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

    def __init__(self, methodName='runTest'):
        super(TestDiary, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # tasks
        result = self.runner.invoke(yoda.cli, ['diary', 'tasks'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="2")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nt'], input="test task")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nt'], input="test task 2")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="2")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="3")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'tasks'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'analyze'])
        self.assertEqual(result.exit_code, 0)

        # notes
        result = self.runner.invoke(yoda.cli, ['diary', 'notes'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nn'], input="test note")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nn'], input="test note")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'notes'])
        self.assertEqual(result.exit_code, 0)
