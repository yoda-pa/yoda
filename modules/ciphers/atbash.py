import string

import click

class AtbashCipher:
    """
    A class which implements the Atbash Cipher
    """

    def __init__(self):
        """
        Calculates the key dictionary.
        """
        self.alphabet = string.ascii_uppercase
        reverse_alphabet = self.alphabet[::-1]
        self.key = {" ": " "}

        for index, char in enumerate(self.alphabet):
            self.key[char] = reverse_alphabet[index]

    def encrypt(self, message):
        """
        Atbash Cipher encryption.
        """
        encrypted_message = ""
        message = message.upper()

        for char in message:
            if char not in self.alphabet and char != " ":
                click.echo("Atbash only supports ASCII characters.")
                return

            encrypted_message += self.key[char]
        return encrypted_message
    
    def decrypt(self, message):
        """
        As the encrypt and the decrypt "key" are the 
        same encrypt is its own inverse function.
        """
        return self.encrypt(message)