import numpy as np
import click
import string

class HillCipher:
    """
    A class which implements the Hill Cipher.
    """
    def __init__(self, key_matrix):
        self.key_matrix = key_matrix

    def encrypt(self, message):
        """
        Encrypts the text using the Hill Cipher.
        """
        message = message.upper()
        message = message.replace(" ", "")  # Remove spaces
        message = [ord(char) - ord('A') for char in message]

        encrypted_text = ""
        for i in range(0, len(message), len(self.key_matrix)):
            block = message[i:i+len(self.key_matrix)]
            if len(block) < len(self.key_matrix):
                # Padding if necessary
                block += [0] * (len(self.key_matrix) - len(block))
            block = np.array(block)
            encrypted_block = np.dot(self.key_matrix, block) % 26
            encrypted_text += "".join(chr(char + ord('A')) for char in encrypted_block)

        return encrypted_text

    def decrypt(self, message):
        """
        Decrypts the text using the Hill Cipher.
        """
        message = message.upper()
        message = message.replace(" ", "")  # Remove spaces
        message = [ord(char) - ord('A') for char in message]

        decrypted_text = ""
        inverse_key_matrix = np.linalg.inv(self.key_matrix)
        determinant = int(round(np.linalg.det(self.key_matrix))) % 26

        for i in range(0, len(message), len(self.key_matrix)):
            block = message[i:i+len(self.key_matrix)]
            if len(block) < len(self.key_matrix):
                # Padding if necessary
                block += [0] * (len(self.key_matrix) - len(block))
            block = np.array(block)
            decrypted_block = np.dot(inverse_key_matrix, block) % 26
            decrypted_text += "".join(chr(char + ord('A')) for char in decrypted_block)

        return decrypted_text

# Example key matrix (3x3)
key_matrix = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])

hill_cipher = HillCipher(key_matrix)

if __name__ == "__main__":
    choice = click.prompt("Encrypt (e) or Decrypt (d)?")
    message = click.prompt("Enter the message")

    if choice == "e":
        encrypted_text = hill_cipher.encrypt(message)
        click.echo(f"Encrypted text: {encrypted_text}")
    elif choice == "d":
        decrypted_text = hill_cipher.decrypt(message)
        click.echo(f"Decrypted text: {decrypted_text}")
    else:
        click.echo("Invalid choice")
