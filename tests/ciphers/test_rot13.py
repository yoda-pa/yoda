# coding=utf-8
import unittest
from click.testing import CliRunner

import yoda


class TestRot13(unittest.TestCase):
    """
        Test for the following commands:

        | Module: ciphers
        | command: ciphers
        | args: encrypt
        | input: 1 <text>
    """

    def __init__(self, methodName="runTest"):
        super(TestRot13, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # testing for invalid text input for rot13 encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="1\n$#$#")
        self.assertNotEquals(result.exit_code, 0)

        # testing for invalid text input for rot13 decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="1\n12345")
        self.assertNotEquals(result.exit_code, 0)

        # testing for working rot13 encryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "encrypt"],
                                    input="1\nsample")
        self.assertEqual(result.exit_code, 0)

        # testing for working rot13 decryption
        result = self.runner.invoke(yoda.cli, ["ciphers", "decrypt"],
                                    input="1\nsample")
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
