# coding=utf-8
from builtins import str
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestDictionary(TestCase):
    """
        Test for the following commands:

        | Module: learn
        | command: define, synonym, antonym, example
    """

    def __init__(self, methodName='runTest'):
        super(TestDictionary, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['dictionary', 'define', 'fat'])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode('ascii', 'ignore'))
        self.assertEqual(type(output_string), str)

        result = self.runner.invoke(yoda.cli, ['dictionary', 'synonym', 'fat'])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode('ascii', 'ignore'))
        self.assertEqual(type(output_string), str)

        result = self.runner.invoke(yoda.cli, ['dictionary', 'antonym', 'fat'])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode('ascii', 'ignore'))
        self.assertEqual(type(output_string), str)

        result = self.runner.invoke(yoda.cli, ['dictionary', 'example', 'fat'])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode('ascii', 'ignore'))
        self.assertEqual(type(output_string), str)
