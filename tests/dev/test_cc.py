# coding=utf-8
import os
import json
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestCC(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: cc
    """

    def __init__(self, methodName='runTest'):
        super(TestCC, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['cc', 'ls'])
        self.assertTrue(os.path.exists("resources/custom_commands/custom_commands.json"))

        with open('resources/custom_commands/custom_commands.json') as f:
            data = json.load(f)
            self.assertTrue('ls' in data)

        result = self.runner.invoke(yoda.cli, ['cc', 'ls'])
        self.assertEqual(0, result.exit_code)
