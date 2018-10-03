from __future__ import absolute_import
from __future__ import division

import collections
import json
import re
import itertools
import string
import sys

from builtins import range
from builtins import str

import pyspeedtest
import os
import requests

from past.utils import old_div

from .util import *
from .alias import alias_checker

FIREBASE_DYNAMIC_LINK_API_KEY = "AIzaSyAuVJ0zfUmacDG5Vie4Jl7_ercv6gSwebc"
GOOGLE_URL_SHORTENER_API_KEY = "AIzaSyCBAXe-kId9UwvOQ7M2cLYR7hyCpvfdr7w"
domain = "yodacli.page.link"

@click.group()
def dev():
    """
        Dev command group:\n
        contains commands helpful for developers
    """


@dev.command()
def speedtest():
    """
    Run a speed test for your internet connection
    """
    os.system("speedtest-cli")



# code for URL command


def url_shorten(url_to_be_shortened):
    """
    shorten url
    :param url_to_be_shortened:
    """
    try:
        r = requests.post('https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=' + FIREBASE_DYNAMIC_LINK_API_KEY,
                          data=json.dumps({"dynamicLinkInfo": {"dynamicLinkDomain": domain,"link": url_to_be_shortened }}), headers={
                'Content-Type': 'application/json'
            })
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    response = 'Here\'s your shortened URL:\n' + data['shortLink']
    click.echo(response)


def url_expand(url_to_be_expanded):
    """
    expander
    :param url_to_be_expanded:
    """
    try:
        r = requests.get(
            'https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTENER_API_KEY +
            '&shortUrl=' + url_to_be_expanded)
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    res = data['longUrl']
    if domain in data['longUrl']:
        res = data['longUrl'].split('=')[1]
        #res = res[:-3]
    response = 'Here\'s your original URL:\n' + res
    click.echo(response)


def check_sub_command_url(action, url_to_be_expanded_or_shortened):
    """
    command checker for url shortener and expander
    :param action:
    :param url_to_be_expanded_or_shortened:
    :return:
    """
    sub_commands = {
        'shorten': url_shorten,
        'expand': url_expand
    }
    try:
        return sub_commands[action](url_to_be_expanded_or_shortened)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda url --help" for more info')


@dev.command()
@click.pass_context
@click.argument('input', nargs=1, required=False, callback=alias_checker)
@click.argument('url', nargs=1, required=False, callback=alias_checker)
def url(ctx, input, url):
    """
        URL shortener and expander\n\n
        Commands:
        shorten: to shorten the given URL
        expand: to expand shortened URL
    """
    input, url = get_arguments(ctx, 2)
    _input = str(input)
    _url = str(url)
    check_sub_command_url(_input, _url)


@dev.command()
def hackernews():
    """
    Hacker news top headlines
    """
    _url = 'https://newsapi.org/v2/everything?sources=hacker-news&apiKey=534594afc0d64a11819bb83ac1df4245'
    response = requests.get(_url)
    result = response.json()
    if result['status'] == 'ok':
        for index, item in enumerate(result['articles']):
            counter = '{}/{} \n'.format((index + 1), len(result['articles']))

            title = item['title'] or 'No title'
            description = item['description'] or 'No description'
            url = item['url'] or 'No url'

            click.echo('News-- ' + counter)
            click.echo('Title--  ' + title)
            click.echo('Description-- ' + description)
            click.echo('url-- ' + url)
            click.echo()
            click.echo('Continue? [press-"y"] ')
            c = click.getchar()
            click.echo()  # newline after news item
            if c != 'y':
                break
    else:
        click.echo('Error in api')


@dev.command()
def coinflip():
    """
    Flips a coin and displays an outcome
    """
    import random
    side = random.randint(1, 100) % 2
    click.echo('Heads' if side == 1 else 'Tails')


@dev.command()
def portscan():
    """
    Scan open ports of a website,
    utilizing multi-threading to speed the task along
    """
    import threading
    import re
    is_py2 = sys.version[0] == '2'
    if is_py2:
        import Queue as queue
    else:
        import queue as queue

    def scanPortsTask(port):
        import socket

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.settimeout(1.0)
        try:
            socket.connect((targetForScan, port))
            with lock_output:
                click.echo('port:' + str(port) + ' is open')

        except Exception as e:
            pass

    def taskMaster():

        while True:
            port = port_queue.get()
            scanPortsTask(port)
            port_queue.task_done()

    lock_output = threading.Lock()
    port_queue = queue.Queue()
    targetForScan = input('Where scan ports, should I: ')
    pattern = '([\da-z\.-]+)\.([a-z\.]{2,6})$'

    if re.match(pattern, targetForScan):
        for x in range(200):
            t = threading.Thread(target=taskMaster)

            t.daemon = True
            t.start()

        for worker in range(1, 1000):
            port_queue.put(worker)

        port_queue.join()
    else:
        click.echo('Find ' + targetForScan + ' I cannot, ' + 'sure spelled correctly, are you?')


@dev.command()
@click.pass_context
@click.argument('ip_address', nargs=1, required=False, callback=alias_checker)
def iplookup(ctx, ip_address):
    """
    Find the geographical location of a given IP address.
    """
    # import pdb; pdb.set_trace()
    ip_address = get_arguments(ctx, 1)
    if not ip_address:
        return click.echo('Please supply an IP address as follows: $ yoda iplookup <ip_address>')

    _ip_address = str(ip_address)

    import geoip2.database

    path = os.path.dirname(sys.modules['yoda'].__file__)
    path = os.path.join(path, 'resources/databases/GeoLite2-City.mmdb')

    reader = geoip2.database.Reader(path)
    response = reader.city(_ip_address)
    return click.echo('{0}, {1}'.format(response.subdivisions.most_specific.name, response.country.name))


@dev.command()
@click.pass_context
@click.argument('link', nargs=1, required=True)
def checksite(ctx, link):
    """
    Check if website is up and running.
    """
    click.echo('Connecting...')

    # request
    try:
        r = requests.get(link)
    except Exception as e:
        click.echo('Looks like {0} is not a valid URL, check the URL and try again.'.format(link))
        return

    # check the status code
    if r.status_code != 200:
        click.echo("Uh-oh! Site is down. :'(")
    else:
        click.echo('Yay! The site is up and running! :)')
 
@dev.command()
@click.pass_context
@click.argument('astrological_sign', nargs=1, required=False, callback=alias_checker)
def horoscope(ctx, astrological_sign):
    """
    Find the today's horoscope for the given astrological sign.
    """
    astrological_sign = get_arguments(ctx, 1)
    _astrological_sign = str(astrological_sign)

    try:
        r = requests.get('http://horoscope-api.herokuapp.com/horoscope/today/{0}'.format(astrological_sign))
        return click.echo(r.json()['horoscope'])
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

# idea list process
@dev.command()
@click.argument('pattern', nargs=1)
@click.argument('path', nargs=1)
@click.option('-r', nargs=1, required=False, default=False)
@click.option('-i', nargs=1, required=False, default=False)
def grep(pattern, path, r, i):
    """
        Grep for a pattern in a file or recursively through a folder.
        yoda dev grep PATTERN PATH [OPTIONAL ARGUMENTS]
    """
    recursive, ignorecase = r, i
    if ignorecase:
        pattern = re.compile(pattern, flags=re.IGNORECASE)
    else:
        pattern = re.compile(pattern)
    if os.path.isfile(path):
        if recursive:
            click.echo(chalk.red(
                'Cannot use recursive flag with a file name.'))
            return
        with open(path, 'r') as infile:
            for match in search_file(pattern, infile):
                click.echo(match, nl=False)
    else:
        for dirpath, dirnames, filenames in os.walk(path, topdown=True):
            for filename in filenames:
                with open(os.path.join(dirpath, filename), 'r') as infile:
                    for match in search_file(pattern, infile):
                        click.echo(match, nl=False)
            if not recursive:
                break


def search_file(pattern, infile):
    for line in infile:
        match = pattern.search(line)
        if match:
            yield line

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

    


@dev.command()
@click.pass_context
@click.argument('mode', nargs=1, required=False, callback=alias_checker)
def ciphers(ctx, mode):
    """
    Encrypts and decrypts texts in classical ciphers
    """

    mode = get_arguments(ctx, 1)
    _mode = str(mode).lower()
    
    cipher_dict = {
                    "Atbash": AtbashCipher,
                    "Caesar": CaesarCipher,
                    "ROT13": ROT13Cipher
                }

    for index, cipher in enumerate(cipher_dict):
        print("{0}: {1}".format(index, cipher))

    cipher_choice = int(click.prompt("Choose a cipher"))
    if cipher_choice > len(cipher_dict) - 1 or cipher_choice < 0:
        click.echo("Invalid cipher number was chosen.")
        return

    cipher = cipher_dict[list(cipher_dict.keys())[cipher_choice]]()

    if _mode == "encrypt":
        clear_text = click.prompt("The text you want to encrypt")
        return click.echo(cipher.encrypt(clear_text))
    elif _mode == "decrypt":
        cipher_text = click.prompt("The text you want to decrypt")
        return click.echo(cipher.decrypt(cipher_text))
    else:
        return click.echo("Invalid mode passed.")


