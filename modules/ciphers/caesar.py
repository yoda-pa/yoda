import collections
import itertools
import string

import click

class CaesarCipher:
    """
    A class which implements the Caesar Cipher.
    """
    def encrypt(self, message):
        """
        Asks the user for the alphabet shift and then encrypts the text.
        """
        message = message.upper()
        shift = int(click.prompt("The shift value"))
        encryption_dictionary, _ = self.generate_alphabets(shift)
        encrypted_text = ""

        for char in message:
            if char not in string.ascii_uppercase and char != " ":
                click.echo("The Caesar Cipher only supports ASCII characters")
                return

            if char == " ":
                encrypted_text += " "
            else:
                encrypted_text += encryption_dictionary[char]
        return encrypted_text
    
    def decrypt(self, message):
        """
        Asks the user for the alphabet shift and then decrypts the text.
        """
        message = message.upper()

        shift = int(click.prompt("The shift value"))
        _, decryption_dictionary = self.generate_alphabets(shift)
        decrypted_text = ""

        for char in message:
            if char not in string.ascii_uppercase and char != " ":
                click.echo("The Caesar Cipher only supports ASCII characters")
                return

            if char == " ":
                decrypted_text += " "
            else:
                decrypted_text += decryption_dictionary[char]
        return decrypted_text
    
    def generate_alphabets(self, shift):
        """
        Generates an en and decryption alphabet for a shift.
        """
        clear_text_alphabet = list(string.ascii_uppercase)
        encryption_alphabet = collections.deque(clear_text_alphabet)
        encryption_alphabet.rotate(shift)
        encryption_alphabet = list(encryption_alphabet)


        encryption_dictionary = dict(itertools.izip(encryption_alphabet, clear_text_alphabet))
        decryption_dictionary = dict(itertools.izip(clear_text_alphabet, encryption_alphabet))
        return encryption_dictionary, decryption_dictionary