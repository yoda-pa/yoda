# Morse coder and decoder

import click

ALPHANUM_TO_MORSE_DICT = {'A': '.-',     'B': '-...',   'C': '-.-.',
                          'D': '-..',    'E': '.',      'F': '..-.',
                          'G': '--.',    'H': '....',   'I': '..',
                          'J': '.---',   'K': '-.-',    'L': '.-..',
                          'M': '--',     'N': '-.',     'O': '---',
                          'P': '.--.',   'Q': '--.-',   'R': '.-.',
                          'S': '...',    'T': '-',      'U': '..-',
                          'V': '...-',   'W': '.--',    'X': '-..-',
                          'Y': '-.--',   'Z': '--..',

                          ' ': ' ',

                          '0': '-----',  '1': '.----',  '2': '..---',
                          '3': '...--',  '4': '....-',  '5': '.....',
                          '6': '-....',  '7': '--...',  '8': '---..',
                          '9': '----.'
                          }

# Reversed initial dictionary
MORSE_TO_ALPHANUM_DICT = {v: k for k, v in ALPHANUM_TO_MORSE_DICT.items()}


def code(message):

    message = message.upper()
    coded_message = ''

    for char in message:
        try:
            coded_message += ALPHANUM_TO_MORSE_DICT[char] + ' '
        except KeyError:
            print('Only alphanumeric characters.')

    return coded_message


def decode(message):

    message = message.upper().split()
    decoded_message = ''

    for code in message:
        try:
            decoded_message += MORSE_TO_ALPHANUM_DICT[code]
        except KeyError:
            print('Only alphanumeric characters.')

    return decoded_message


def ask_for_message():
    message = click.prompt("What's your message?")
    return message


action = click.prompt('Do you want to code or decode a message? [C / D]').lower()

while action != 'c' and action != 'd':
    action = click.prompt('Please, enter C for code or D for decode').lower()

if action == 'c':

    message = ask_for_message()
    coded_message = code(message)

    print(coded_message)
    exit()

if action == 'd':

    message = ask_for_message()
    decoded_message = decode(message)

    print(decoded_message)
    exit()
    
