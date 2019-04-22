import collections
import itertools
import string
from collections import deque

import click

class VigenereCipher:
    """
    A class which implements the vigenere Cipher.
    """
    def __init__(self):
        """
        sets ascii limitations
        """
        self.ascii_A = ord('A')
        self.ascii_threshold = 26 # number of uppercase ascii letters
        self.ascii_error_message = "The Vigenere Cipher only supports ASCII characters"

    def make_shift_queue(self, keyword, mode):
        """
        turns a keyword into a queue of shift values. 
        mode determines whether the shift values are for
        encryption or decryption
        valid values are mode='enc' and mode='dec'
        """
        vigenere_queue = deque() #queue to hold the shift values

        shift_dir = 1
        if mode=='dec':
            shift_dir = -1  #will cause the shifts to be reversed
                            #allowing for easy decryption
        for char in keyword:
            if char not in string.ascii_uppercase and char != " ":
                return -1
            #A should shift by 1, B by 2 ... Z by 26
            #print(ord(char) - ascii_A)
            if char != " ":
                vigenere_queue.append(shift_dir*(ord(char) - self.ascii_A +1))
        return vigenere_queue

    def shift_char(self, char, vigenere_queue):
        """
        returns the ascii character resulting from shifting char by the next value in the keyword queue
        """
        shift = vigenere_queue.popleft()
        vigenere_queue.append(shift) #returns shift value to back of queue in case it is needed again
        return chr(((ord(char) - self.ascii_A + shift ) % self.ascii_threshold) + self.ascii_A)
        

    def encrypt(self, message):
        """
        Asks the user for the alphabet shift and then encrypts the text.
        """
        message = message.upper()
        keyword = str(click.prompt("The encryption keyword"))
        keyword = keyword.upper()
        encrypted_text = ""

        vigenere_queue = self.make_shift_queue(keyword, 'enc')  
        if vigenere_queue == -1:  
            click.echo(self.ascii_error_message)
            return    

        for char in message:
            if char not in string.ascii_uppercase and char != " ":
                click.echo(self.ascii_error_message)
                return
            if char == " ":
                encrypted_text += " "
            else:
                encrypted_text += self.shift_char(char, vigenere_queue)
                
    
        return encrypted_text
    
    def decrypt(self, message):
        """
        Asks the user for the alphabet shift and then decrypts the text.
        """
        message = message.upper()

        keyword = str(click.prompt("The decryption keyword"))
        keyword = keyword.upper()
        
        vigenere_queue = self.make_shift_queue(keyword, 'dec') 
        if vigenere_queue == -1:  
            click.echo(self.ascii_error_message)
            return    

        decrypted_text = ""

        for char in message:
            if char not in string.ascii_uppercase and char != " ":
                click.echo(self.ascii_error_message)
                return

            if char == " ":
                decrypted_text += " "
            else:
                decrypted_text += self.shift_char(char, vigenere_queue)
        return decrypted_text