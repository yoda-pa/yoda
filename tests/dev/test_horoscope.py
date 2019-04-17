# coding=utf-8
import sys
from unittest import TestCase
import mock
from click.testing import CliRunner

import yoda
from requests.exceptions import ConnectionError


ARIES_HOROSCOPE_RESULT = {
    u'date': u'2019-03-21', u'sunsign': u'aries',
    u'horoscope': (u'A plain Jane day. Work goes on as usual, and there is'
                   u'progress. But as Ganesha says, it\'s an ordinary day. Hum,'
                   u' whistle, doodle, and sip your green tea. While day '
                   u'dreaming, start planning your dream home. After all, '
                   u'that\'s where the first plan takes shape.')
}


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

        @mock.patch('modules.dev.requests')
        def test_with_correct_input(requests):
            requests.get.json.return_value = ARIES_HOROSCOPE_RESULT
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
