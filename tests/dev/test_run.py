# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda

class TestRun(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: run
    """

    def __init__(self, methodName='runTest'):
        super(TestRun, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['run', 'tests/resources/test_code.py'])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8')).strip()

        result = self.runner.invoke(yoda.cli, ['run', 'no_file.py'])
        self.assertEqual(result.exit_code, 1)
        output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8')).strip()

        result = self.runner.invoke(yoda.cli, ['run', '../logo.png'])
        self.assertEqual(result.exit_code, 1)
        output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8')).strip()
