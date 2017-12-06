# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestDiaryTasks(TestCase):
    """
        Test for the following commands:
        
        Assumes empty diary.

        | Module: diary
        | command: diary tasks, nt, ct
    """

    def __init__(self, methodName='runTest'):
        super(TestDiaryTasks, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['diary', 'tasks'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nt'], input="test task")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'analyze'])
        self.assertEqual(result.exit_code, 0)

class TestDiaryNotes(TestCase):
    """
        Test for the following commands:
        
        Assumes empty diary.

        | Module: diary
        | command: diary notes, nn
    """

    def __init__(self, methodName='runTest'):
        super(TestDiaryNotes, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['diary', 'notes'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nn'], input="test note")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'notes'])
        self.assertEqual(result.exit_code, 0)
