from unittest import TestCase
from click.testing import CliRunner

import yoda

class testVigenere(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: ciphers
        | args: 3 (Vigenere)
    """

    def __init__(self, methodName='runTest'):
        super(testVigenere, self).__init__()
        self.runner = CliRunner()
        self.error_message = "The Vigenere Cipher only supports ASCII characters"

    def runTest(self):
        self.check_sequence("aaaa", "abcd", "BCDE") #simple test
        self.check_sequence("a b c d", " bb", "C D E F") #test spaces
        self.check_sequence("mnop", "ab", "NPPR") #test key reuse
        self.check_sequence("axyz", "b", "CZAB") #test wraparound
        self.check_sequence("aaa4a", "abcd", self.error_message)#invalid plaintext
        self.check_sequence("aaaa", "ab4d", self.error_message)#invalid key
        

    def check_sequence(self, plaintext, keyword, encrypted):
        #check encryption
        input = plaintext
        expected_output = encrypted
        self.check_sequence_helper(input, keyword, expected_output, "encrypt")

        if(encrypted != self.error_message):
            input = encrypted
            expected_output = plaintext

        self.check_sequence_helper(input, keyword, expected_output, "decrypt")

        #check corresponding decryption

    def check_sequence_helper(self, input, keyword, expected_output, mode):
        result = self.runner.invoke(yoda.cli, ["ciphers", mode],
                                input="3\n"+input+"\n"+keyword)
        self.assertEqual(result.output.strip().splitlines()[-1].upper(), 
                                    expected_output.upper())
