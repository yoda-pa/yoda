# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestChecksite(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: checksite
    """

    def __init__(self, methodName='runTest'):
        super(TestChecksite, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['dev', 'checksite', 'https://google.com'])
        output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8')).strip()
        self.assertTrue("running" in output_string)
