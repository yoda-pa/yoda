import click
import chalk
import getpass
import lepl.apps.rfc3696
import yaml
import os.path
from Crypto.Cipher import AES
import string
import random
from config import config_file_paths

CONFIG_FILE_PATH = config_file_paths['CONFIG_FILE_PATH']

# used to generate key and IV456 for Crypto


def cypher_pass_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# to encrypt the password


def encrypt_password(cipher_key, cipher_IV456, password):
    return AES.new(cipher_key, AES.MODE_CBC, cipher_IV456).encrypt(password * 16)

# to decrypt the password from the cipher text. written to test the
# functionality of pycrypto


def decrypt_password():
    config_file = open(CONFIG_FILE_PATH, 'r')
    contents = yaml.load(config_file)
    cipher_key = contents['encryption']['cipher_key']
    cipher_IV456 = contents['encryption']['cipher_IV456']
    ciphertext = contents['github']['password']
    s = AES.new(cipher_key, AES.MODE_CBC, cipher_IV456).decrypt(ciphertext)
    return s[:len(s) / 16]

# create new config file


def new():
    chalk.blue('Enter your name:')
    name = raw_input().strip()
    while len(name) == 0:
        chalk.red("You entered nothing!")
        chalk.blue('Enter your name:')
        name = raw_input().strip()

    chalk.blue('What\'s your email id?')
    email = raw_input().strip()
    email_validator = lepl.apps.rfc3696.Email()
    while not email_validator(email):
        chalk.red("Invalid email ID!")
        chalk.blue('What\'s your email id?')
        email = raw_input().strip()

    chalk.blue('What\'s your github username?')
    gh_username = raw_input().strip()
    while len(gh_username) == 0:
        chalk.red("You entered nothing!")
        chalk.blue('What\'s your github username?')
        gh_username = raw_input().strip()

    chalk.blue('Enter your github password:')
    gh_password = getpass.getpass()
    while len(gh_password) == 0:
        chalk.red("You entered nothing!")
        chalk.blue('Enter your github password:')
        gh_password = getpass.getpass()
    # let's encrypt our password
    cipher_key = cypher_pass_generator()
    cipher_IV456 = cypher_pass_generator()

    encrypted_gh_password = encrypt_password(
        cipher_key, cipher_IV456, gh_password)

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
        chalk.red(
            'A configuration file already exists. Are you sure you want to overwrite it? (y/n)')
        overwrite_response = raw_input().lower()
        if not (overwrite_response == 'y' or overwrite_response == 'yes'):
            return

    with open(CONFIG_FILE_PATH, 'w') as config_file:
        yaml.dump(setup_data, config_file, default_flow_style=False)

# check existing setup


def check():
    # TODO: beautify output
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            contents = yaml.load(config_file)
            click.echo('Name: ' + contents['name'])
            click.echo('Email: ' + contents['email'])
            click.echo('Github username: ' + contents['github']['username'])

            # click.echo(decrypt_password())
    else:
        chalk.red(
            'The configuration file does not exist. Please type "yoda setup new" to create a new one')

# delete config_file


def delete():
    if os.path.isfile(CONFIG_FILE_PATH):
        chalk.red('Are you sure you want to delete previous configuration? (y/n)')
        delete_response = raw_input().lower().strip()
        if delete_response != 'y':
            click.echo('Operation cancelled')
            return
        os.remove(CONFIG_FILE_PATH)
        chalk.red('Configuration file deleted')
    else:
        chalk.red('Configuration file does not exist!')

# checks which command to execute


def check_sub_command(c):
    sub_commands = {
        'new': new,
        'check': check,
        'delete': delete
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "yoda setup --help" for more info')


def get_gh_username():
    config_file = open(CONFIG_FILE_PATH, 'r')
    contents = yaml.load(config_file)
    return contents['github']['username']

# the main process


def process(input):
    input = input.lower().strip()
    # check which command to execute
    check_sub_command(input)
