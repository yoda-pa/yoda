# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestLeaselist(TestCase):
    """
        Test for the following commands:

        | Module: leaselist
        | commands: show, add, remove
    """

    def __init__(self, methodName="runTest"):
        super(TestLeaselist, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["leaselist", "show"], input="n")
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["leaselist", "add"], input="l\ntestitem\nhuman\n09/09/2019")
        self.assertEqual(result.exit_code, 0)
        # output_string = str(result.output.encode('ascii', 'ignore'))
        # print(output_string)
        
        result = self.runner.invoke(yoda.cli, ["leaselist", "remove"], input="1")
        self.assertEqual(result.exit_code, 0)

        pass
