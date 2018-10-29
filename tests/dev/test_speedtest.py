# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestSpeedtest(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: speedtest
    """

    def __init__(self, methodName="runTest"):
        super(TestSpeedtest, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["speedtest"])
        print(
            "------============------============------============------============------============------============------============"
        )
        print(str(result.output.encode("ascii", "ignore")))
        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)
