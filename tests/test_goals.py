# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import tempfile
import os

import yoda
from modules import config


class TestGoals(TestCase):
    """
        Test for the following commands:

        Assumes empty goals list.

        | Module: goals
        | command: goals new, view, tasks, complete, analyze
    """

    def __init__(self, methodName='runTest'):
        super(TestGoals, self).__init__()
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

        result = self.runner.invoke(yoda.cli, ['goals'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['goals', 'view'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['goals', 'new'], input="test\ntest goal\n2020-02-02")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['goals', 'view'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['goals', 'tasks'], input="test")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['goals', 'complete'], input="1")
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(yoda.cli, ['goals', 'analyze'])
        self.assertEqual(result.exit_code, 0)