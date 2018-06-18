from __future__ import division
from __future__ import absolute_import
from builtins import input
from builtins import range
from past.utils import old_div
import errno
import getpass
import os.path
import random
import string

import chalk
import click
import lepl.apps.rfc3696
import yaml
from Crypto.Cipher import AES

from .config import get_config_file_paths
from .config import update_config_path

CONFIG_FILE_PATH = get_config_file_paths()['USER_CONFIG_FILE_PATH']

try:
    raw_input          # Python 2
except NameError:
    raw_input = input  # Python 3


def cypher_pass_generator(size=16, chars=string.ascii_uppercase + string.digits):
    """
    used to generate key and IV456 for Crypto
    :param size:
    :param chars:
    :return:
    """
    return ''.join(random.choice(chars) for _ in range(size))


def encrypt_password(cipher_key, cipher_IV456, password):
    """
    to encrypt the password
    :param cipher_key:
    :param cipher_IV456:
    :param password:
    :return:
    """
    return AES.new(cipher_key, AES.MODE_CBC, cipher_IV456).encrypt(password * 16)


def decrypt_password():
    """
    to decrypt the password from the cipher text. written to test the
    functionality of pycrypto
    :return:
    """
    config_file = open(CONFIG_FILE_PATH)
    contents = yaml.load(config_file)
    cipher_key = contents['encryption']['cipher_key']
    cipher_IV456 = contents['encryption']['cipher_IV456']
    cipher_text = contents['github']['password']
    s = AES.new(cipher_key, AES.MODE_CBC, cipher_IV456).decrypt(cipher_text)
    return s[:old_div(len(s), 16)]


def new():
    """
    create new config file
    :return:
    """
    click.echo(chalk.blue('Enter your name:'))
    name = input().strip()
    while len(name) == 0:
        click.echo(chalk.red("You entered nothing!"))
        click.echo(chalk.blue('Enter your name:'))
        name = input().strip()

    click.echo(chalk.blue('What\'s your email id?'))
    email = input().strip()
    email_validator = lepl.apps.rfc3696.Email()
    while not email_validator(email):
        click.echo(chalk.red("Invalid email ID!"))
        click.echo(chalk.blue('What\'s your email id?'))
        email = input().strip()

    click.echo(chalk.blue('What\'s your github username?'))
    gh_username = input().strip()
    while len(gh_username) == 0:
        click.echo(chalk.red("You entered nothing!"))
        click.echo(chalk.blue('What\'s your github username?'))
        gh_username = input().strip()

    click.echo(chalk.blue('Enter your github password:'))
    gh_password = getpass.getpass()
    while len(gh_password) == 0:
        click.echo(chalk.red("You entered nothing!"))
        click.echo(chalk.blue('Enter your github password:'))
        gh_password = getpass.getpass()
    # let's encrypt our password
    cipher_key = cypher_pass_generator()
    cipher_IV456 = cypher_pass_generator()

    encrypted_gh_password = encrypt_password(
        cipher_key, cipher_IV456, gh_password)

    click.echo(chalk.blue('Where shall your config be stored? (Default: ~/.yoda/)'))
    # because os.path.isdir doesn't expand ~
    config_path = os.path.expanduser(input().strip())
    while not os.path.isdir(config_path):
        if len(config_path) == 0:
            break
        click.echo(chalk.red('Path doesn\'t exist!'))
        click.echo(chalk.blue('Where shall your config be stored? (Default: ~/.yoda/)'))
        config_path = os.path.expanduser(input().strip())

    update_config_path(config_path)
    CONFIG_FILE_PATH = get_config_file_paths()['USER_CONFIG_FILE_PATH']

    setup_data = dict(
        name=name,
        email=email,
        github=dict(
            username=gh_username,
            password=encrypted_gh_password
        ),
        encryption=dict(
            cipher_key=cipher_key,
            cipher_IV456=cipher_IV456
        )
    )

    if not os.path.exists(os.path.dirname(CONFIG_FILE_PATH)):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE_PATH))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if os.path.isfile(CONFIG_FILE_PATH):
        click.echo(chalk.red(
            'A configuration file already exists. Are you sure you want to overwrite it? (y/n)'))
        overwrite_response = input().lower()
        if not (overwrite_response == 'y' or overwrite_response == 'yes'):
            return

    with open(CONFIG_FILE_PATH, 'w') as config_file:
        yaml.dump(setup_data, config_file, default_flow_style=False)


def check():
    """
    check existing setup
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH) as config_file:
            contents = yaml.load(config_file)
            click.echo('Name:            ' + contents['name'])
            click.echo('Email:           ' + contents['email'])
            click.echo('Github username: ' + contents['github']['username'])

            # click.echo(decrypt_password())
    else:
        click.echo(chalk.red(
            'The configuration file does not exist. Please type "yoda setup new" to create a new one'))


def delete():
    """
    delete config_file
    :return:
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        click.echo(chalk.red('Are you sure you want to delete previous configuration? (y/n)'))
        delete_response = input().lower().strip()
        if delete_response != 'y':
            click.echo('Operation cancelled')
            return
        os.remove(CONFIG_FILE_PATH)
        click.echo(chalk.red('Configuration file deleted'))
    else:
        click.echo(chalk.red('Configuration file does not exist!'))


def check_sub_command(c):
    """
    checks which command to execute
    :param c:
    :return:
    """
    sub_commands = {
        'new': new,
        'check': check,
        'delete': delete
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda setup --help" for more info')


def get_gh_username():
    """
    get github username
    :return:
    """
    config_file = open(CONFIG_FILE_PATH)
    contents = yaml.load(config_file)
    return contents['github']['username']


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    # check which command to execute
    check_sub_command(_input)
