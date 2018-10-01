# coding=utf-8
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
        self.assertTrue(type(result.output.encode('ascii', 'ignore').decode('utf-8')) == unicode)
