import click
import chalk
import yaml
import apiai
import config
import json
from forex_python.converter import CurrencyRates, CurrencyCodes

from config import config_file_paths
from util import *

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get('API_AI_SESSION_ID', config.API_AI_SESSION_ID)

# config file path
MONEY_CONFIG_FILE_PATH = config_file_paths['MONEY_CONFIG_FILE_PATH']
MONEY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(MONEY_CONFIG_FILE_PATH)

# currency converter
currency_rates = CurrencyRates()
currency_codes = CurrencyCodes()

# check status of setup
def status():
    if os.path.isfile(MONEY_CONFIG_FILE_PATH):
        with open(MONEY_CONFIG_FILE_PATH, 'r') as config_file:
            contents = yaml.load(config_file)
            click.echo(contents)
    else:
        click.echo('The configuration file for this module does not exist. Please type "dude money setup" to create a new one')

# create new setup config
def setup():
    create_folder(MONEY_CONFIG_FOLDER_PATH)

    if ask_overwrite(MONEY_CONFIG_FILE_PATH):
        return

    chalk.blue('Enter default currency code:')
    currency_code = (raw_input().strip())
    click.echo(currency_rates.get_rates(currency_code))
    click.echo(currency_codes.get_symbol(currency_code))
    click.echo(currency_codes.get_currency_name(currency_code))

    chalk.blue('Enter inital amount:')
    initial_money = int(raw_input().strip())

    setup_data = dict (
        currency_code = currency_code,
        initial_money = initial_money
    )

    input_data(setup_data, MONEY_CONFIG_FILE_PATH)

def expense():
    request.query = raw_input()
    click.echo('output: ')
    response = request.getresponse().read()
    output = json.loads(response)
    click.echo(output)

# command checker
def check_sub_command(c):
    sub_commands = {
        'status' : status,
        'setup' : setup,
        'exp' : expense
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude money --help" for more info')

# the main process
def process(input):
    input = input.lower().strip()
    check_sub_command(input)
