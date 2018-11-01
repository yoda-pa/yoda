# coding=utf-8
import sys
from unittest import TestCase
import mock
from click.testing import CliRunner

import yoda
from requests.exceptions import ConnectionError

def function_with_connection_error():
    raise ConnectionError()

class TestHoroscope(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: horoscope
    """

    def __init__(self, methodName="runTest"):
        super(TestHoroscope, self).__init__()
        self.runner = CliRunner()

    def runTest(self):

        def test_with_correct_input():
            result = self.runner.invoke(yoda.cli, ['horoscope', 'aries'])
            if sys.version_info[0] == 3:
                string_types = str
            else:
                string_types = basestring

            self.assertIsInstance(result.output, string_types)
            self.assertEqual(result.exit_code, 0)

        @mock.patch('requests.get', side_effect=function_with_connection_error)
        def test_with_connection_error(_self):
            result = self.runner.invoke(yoda.cli, ['horoscope', 'aries'])
            self.assertEqual(result.exit_code, -1)

        test_with_correct_input()
        test_with_connection_error()
