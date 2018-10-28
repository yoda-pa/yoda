# coding=utf-8
from unittest import TestCase
import mock
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
        empty_response_json = {}

        def test_with_correct_file_path():
            result = self.runner.invoke(yoda.cli, ['fileshare', 'logo.png'])
            self.assertEqual(result.exit_code, 0)

        def test_with_wrong_file_path():
            result = self.runner.invoke(yoda.cli, ['fileshare', 'wrong_path'])
            self.assertEqual(result.exit_code, -1)

        @mock.patch('json.loads', return_value=empty_response_json)
        def test_with_no_key_in_response(_self):
            result = self.runner.invoke(yoda.cli, ['fileshare', 'logo.png'])
            self.assertEqual(result.exit_code, 1)

        test_with_correct_file_path()
        test_with_wrong_file_path()
        test_with_no_key_in_response()
