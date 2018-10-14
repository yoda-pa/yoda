# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class test_fileshare(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: fileshare
        | args: file_path
    """

    def __init__(self, methodName='runTest'):
        super(test_fileshare, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['fileshare', 'logo.png'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ['fileshare', 'wrong_path'])
        self.assertEqual(result.exit_code, 0)
