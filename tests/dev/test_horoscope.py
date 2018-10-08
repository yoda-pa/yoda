# coding=utf-8
import sys
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestHoroscope(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: horoscope
    """

    def __init__(self, methodName='runTest'):
        super(TestHoroscope, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['horoscope', 'aries'])

        if sys.version_info[0] == 3:
            string_types = str
        else:
            string_types = basestring

        self.assertIsInstance(result.output, string_types)
