# coding=utf-8
import unittest
from click.testing import CliRunner

import yoda


class TestInput(unittest.TestCase):
    """
        Test for the following commands:

        | Module: ciphers
        | command: ciphers
        | args: encrypt
        | input: 0 <text> <shift>
    """

    def __init__(self, methodName="runTest"):
        super(TestInput, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # testing for no mode passed for ciphers
        result = self.runner.invoke(yoda.cli, ["ciphers"])
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid cipher input selection in encrypt mode
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="3\nsample\na")
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid cipher input selection in decrypt mode
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="3\nsample\na")
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid cipher mode
        result = self.runner.invoke(yoda.cli, ["ciphers", "abc"],
                                    input="3\nsample\na")
        self.assertNotEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
