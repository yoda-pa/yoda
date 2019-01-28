# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner
import mock

import yoda
from requests.models import Response


class TestChecksite(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: checksite
    """

    def __init__(self, methodName="runTest"):
        super(TestChecksite, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        mocked_response = Response()
        mocked_response.status_code = 400
        
        def test_with_working_url():
            result = self.runner.invoke(yoda.cli, ['dev', 'checksite', 'https://google.com'])
            output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8')).strip()
            self.assertTrue("running" in output_string)

        def test_with_invalid_url():
            result = self.runner.invoke(yoda.cli, ['dev', 'checksite', 'https://google'])
            self.assertEqual(result.exit_code, -1)

        @mock.patch('requests.get', return_value=mocked_response)
        def test_with_mocked_response_code(_self):
            result = self.runner.invoke(yoda.cli, ['dev', 'checksite', 'https://google.com'])
            self.assertEqual(result.exit_code, 1)

        test_with_working_url()
        test_with_invalid_url()
        test_with_mocked_response_code()
