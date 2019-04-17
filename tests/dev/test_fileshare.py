# coding=utf-8
from unittest import TestCase
import mock
from click.testing import CliRunner

import yoda


FILE_UPLOAD_JSON_RESPONSE = {
    u'link': u'https://file.io/unebeu', u'key': u'unebeu', u'success': True,
    u'expiry': u'14 days'
}


class testFileshare(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: fileshare
        | args: file_path
    """

    def __init__(self, methodName='runTest'):
        super(testFileshare, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        empty_response_json = {}

        @mock.patch('modules.dev.json')
        @mock.patch('modules.dev.requests')
        def test_with_correct_file_path(request, json):
            json.loads.return_value = FILE_UPLOAD_JSON_RESPONSE
            result = self.runner.invoke(yoda.cli, ['fileshare', 'logo.png'])
            self.assertEqual(result.exit_code, 0)

        def test_with_wrong_file_path():
            result = self.runner.invoke(yoda.cli, ['fileshare', 'wrong_path'])
            self.assertEqual(result.exit_code, -1)

        @mock.patch('modules.dev.requests')
        @mock.patch('json.loads', return_value=empty_response_json)
        def test_with_no_key_in_response(_self, requests):
            result = self.runner.invoke(yoda.cli, ['fileshare', 'logo.png'])
            self.assertEqual(result.exit_code, 1)

        test_with_correct_file_path()
        test_with_wrong_file_path()
        test_with_no_key_in_response()
