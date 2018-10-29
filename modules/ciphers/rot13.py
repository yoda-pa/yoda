import collections
import itertools
import string

import click

class ROT13Cipher:
    """
    A class which implements the ROT13 Cipher.
    """
    def __init__(self):
        """
        Calculates the encryption and decryption alphabet
        """
        clear_text_alphabet = list(string.ascii_uppercase)
        encryption_alphabet = collections.deque(clear_text_alphabet)
        encryption_alphabet.rotate(13)
        encryption_alphabet = list(encryption_alphabet)


        self.encryption_dictionary = dict(itertools.izip(encryption_alphabet, clear_text_alphabet))
        self.decryption_dictionary = dict(itertools.izip(clear_text_alphabet, encryption_alphabet))

    def encrypt(self, message):
        """
        ROT13 encryption using the previously generate alphabet.
        """
        message = message.upper()
        encrypted_text = ""

        for char in message:
            if char not in string.ascii_uppercase and char != " ":
                click.echo("The ROT13 Cipher only supports ASCII characters")
                return

            if char == " ":
                encrypted_text += " "
            else:
                encrypted_text += self.encryption_dictionary[char]
        return encrypted_text

    def decrypt(self, message):
        """
        ROT13 encryption using the previously generate alphabet.
        """
        message = message.upper()
        decrypted_text = ""

        for char in message:
            if char not in string.ascii_uppercase and char != " ":
                click.echo("The ROT13 Cipher only supports ASCII characters")
                return

            if char == " ":
                decrypted_text += " "
            else:
                decrypted_text += self.decryption_dictionary[char]
        return decrypted_text