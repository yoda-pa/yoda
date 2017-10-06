import click
import chalk
import yaml
import apiai
import config
import json
import os
from forex_python.converter import CurrencyRates, CurrencyCodes
import time
import datetime
import shlex


from config import get_config_file_paths
import util

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get(
    'API_AI_SESSION_ID', config.API_AI_SESSION_ID)

# config file path
MONEY_CONFIG_FILE_PATH = get_config_file_paths()['MONEY_CONFIG_FILE_PATH']
MONEY_CONFIG_FOLDER_PATH = util.get_folder_path_from_file_path(
    MONEY_CONFIG_FILE_PATH)

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
        click.echo(
            'The configuration file for this module does not exist. Please type "yoda money setup" to create a new one')

# create new setup config


def setup():
    util.create_folder(MONEY_CONFIG_FOLDER_PATH)

    if util.ask_overwrite(MONEY_CONFIG_FILE_PATH):
        return

    chalk.blue('Enter default currency code:')
    currency_code = (raw_input().strip())
    click.echo(currency_rates.get_rates(currency_code))
    click.echo(currency_codes.get_symbol(currency_code))
    click.echo(currency_codes.get_currency_name(currency_code))

    chalk.blue('Enter inital amount:')
    initial_money = int(raw_input().strip())

    setup_data = dict(
        currency_code=currency_code,
        initial_money=initial_money
    )

    util.input_data(setup_data, MONEY_CONFIG_FILE_PATH)


def expense():
    util.create_folder(MONEY_CONFIG_FOLDER_PATH)
    with open(MONEY_CONFIG_FOLDER_PATH + '/expenditures.txt', 'a') as fp:
        request.query = raw_input()
        click.echo('output: ')
        response = request.getresponse().read()
        output = json.loads(response)
        # click.echo(output)
        currency_name = output['result']['parameters']['currency-name']
        item = output['result']['parameters']['any'] if len(
            output['result']['parameters']['any'].split()) == 1 else (
            '"' + output['result']['parameters']['any'] + '"')
        number = output['result']['parameters']['number']

        timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fp.write('{} {} {} {}\n'.format(
            timestamp, currency_name, number, item))


def expenses():
    with open(MONEY_CONFIG_FOLDER_PATH + '/expenditures.txt') as fp:
        for line in fp.read().split('\n'):
            if len(line) == 0:
                continue
            (date, time, currency_name, number, item) = shlex.split(line)
            y, m, d = map(int, date.split('-'))

            if datetime.datetime(
                    y, m, d).month == datetime.datetime.now().month:
                click.echo(date + ' ' + time + ' ' +
                           currency_name + ' ' + number + ' ' + item)

# command checker


def check_sub_command(c):
    sub_commands = {
        'status': status,
        'setup': setup,
        'exp': expense,
        'exps': expenses
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "yoda money --help" for more info')

# the main process


def process(input):
    input = input.lower().strip()
    check_sub_command(input)
