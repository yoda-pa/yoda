# coding=utf-8
from mock import patch
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestSpeedtest(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: speedtest
    """

    def __init__(self, methodName='runTest'):
        super(TestSpeedtest, self).__init__()
        self.runner = CliRunner()

    @patch('modules.dev.os')
    def runTest(self, os):
        result = self.runner.invoke(yoda.cli, ['speedtest'])
        os.system.assert_called_once_with('speedtest-cli')
        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)
