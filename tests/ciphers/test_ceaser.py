# coding=utf-8
import unittest
from click.testing import CliRunner

import yoda


class TestCeaser(unittest.TestCase):
    """
        Test for the following commands:

        | Module: ciphers
        | command: ciphers
        | args: encrypt
        | input: 1 <text> <shift>
    """

    def __init__(self, methodName="runTest"):
        super(TestCeaser, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # testing for invalid shift input for ceaser encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="1\nsample\na")
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid shift input for ceaser decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="1\nsample\na")
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid text input for ceaser encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="1\n$#$#\n3")
        self.assertNotEqual(result.exit_code, 0)

        # testing for invalid text input for ceaser decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="1\n12345\n3")
        self.assertNotEqual(result.exit_code, 0)

        # testing for working ceaser encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="1\nsample\n3")
        self.assertEqual(result.exit_code, 0)

        # testing for working ceaser decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="1\nsample\n3")
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
