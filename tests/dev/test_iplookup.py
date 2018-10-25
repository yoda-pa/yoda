# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestIPLookup(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: iplookup
    """

    def __init__(self, methodName="runTest"):
        super(TestIPLookup, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["iplookup", "128.101.101.101"])
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
        self.assertTrue(output_string == "Minnesota, United States")
