# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import tempfile
import os

import yoda
from modules import config


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

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='yoda_')
        self.original_config_path = config.get_config_folder()
        config.update_config_path(self.tempdir)

    def tearDown(self):
        # Change yoda configuration directory back
        config.update_config_path(self.original_config_path)

        # Delete the temporary directory
        for root, dirs, files in os.walk(self.tempdir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.tempdir)

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['diary'])
        self.assertEqual(result.exit_code, 0)

        # tasks
        result = self.runner.invoke(yoda.cli, ['diary', 'tasks'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="2")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nt'], input="test task\n-")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'ct'], input="1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['diary', 'nt'], input="test task 2\n-")
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