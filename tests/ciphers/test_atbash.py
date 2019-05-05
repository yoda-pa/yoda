# coding=utf-8
import unittest
from click.testing import CliRunner

import yoda


class TestAtbash(unittest.TestCase):
    """
        Test for the following commands:

        | Module: ciphers
        | command: ciphers
        | args: encrypt
        | input: 0 <text>
    """

    def __init__(self, methodName="runTest"):
        super(TestAtbash, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # testing for invalid text input for Atbash encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="0\n$#$#")
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid text input for Atbash decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="0\n12345")
        self.assertNotEqual(result.exit_code, 0)

        # testing for working Atbash encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="0\nsample")
        self.assertEqual(result.exit_code, 0)

        # testing for working Atbash decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="0\nsample")
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
