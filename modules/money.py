from __future__ import absolute_import
from builtins import input
from builtins import map
import datetime
import json
import shlex
import time

import apiai
from forex_python.converter import CurrencyRates, CurrencyCodes

from . import config
from .config import get_config_file_paths
from .util import *

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get(
    'API_AI_SESSION_ID', config.API_AI_SESSION_ID)

# config file path
def get_MONEY_CONFIG_FILE_PATH():
    return get_config_file_paths()['MONEY_CONFIG_FILE_PATH']

def get_MONEY_CONFIG_FOLDER_PATH():
    return get_folder_path_from_file_path(
        get_MONEY_CONFIG_FILE_PATH())

# currency converter
currency_rates = CurrencyRates()
currency_codes = CurrencyCodes()


def __validate_currency_name_and_amount(currency_name, amount):
    """
    Returns true if currency_name and amount contain values.
    These values are already empty at the point this function
    is called if they are invalid, so return false if they do
    not contain values
    :param currency_name:
    :param amount:
    :return:
    """
    if currency_name is None or len(currency_name) == 0 or amount is None or len(amount) == 0:
        return False
    else:
        return True


def status():
    """
    check status of setup
    """
    if os.path.isfile(get_MONEY_CONFIG_FILE_PATH()):
        with open(get_MONEY_CONFIG_FILE_PATH()) as config_file:
            contents = yaml.load(config_file)
            click.echo(contents)
    else:
        click.echo(
            'The configuration file for this module does not exist. Please type "yoda money setup" to create a new one')


def setup():
    """
    create new setup config
    :return:
    """
    create_folder(get_MONEY_CONFIG_FOLDER_PATH())

    if ask_overwrite(get_MONEY_CONFIG_FILE_PATH()):
        return

    click.echo(chalk.blue('Enter default currency code:'))
    currency_code = (input().strip())
    click.echo(currency_rates.get_rates(currency_code))
    click.echo(currency_codes.get_symbol(currency_code))
    click.echo(currency_codes.get_currency_name(currency_code))

    click.echo(chalk.blue('Enter initial amount:'))
    initial_money = int(input().strip())

    setup_data = dict(
        currency_code=currency_code,
        initial_money=initial_money
    )

    input_data(setup_data, get_MONEY_CONFIG_FILE_PATH())


def expense():
    """
    add expense
    """
    create_folder(get_MONEY_CONFIG_FOLDER_PATH())
    with open(get_MONEY_CONFIG_FOLDER_PATH() + '/expenditures.txt', 'a') as fp:
        request.query = input()
        click.echo('output: ')
        response = request.getresponse().read()
        output = json.loads(response)
        # click.echo(output)
        currency_name = output['result']['parameters']['currency-name']
        item = output['result']['parameters']['any'] if len(output['result']['parameters']['any'].split(
        )) == 1 else ('"' + output['result']['parameters']['any'] + '"')
        number = output['result']['parameters']['number']

        timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')

        valid_expense = __validate_currency_name_and_amount(currency_name, number)
        if valid_expense == False:
            click.echo("Invalid Expense!")
        else:
            fp.write('{} {} {} {}\n'.format(
                timestamp, currency_name, number, item))


def expenses():
    """
    check expenses
    """
    with open(get_MONEY_CONFIG_FOLDER_PATH() + '/expenditures.txt') as fp:
        for line in fp.read().split('\n'):
            if len(line) == 0:
                continue
            (date, _time, currency_name, number, item) = shlex.split(line)
            y, m, d = list(map(int, date.split('-')))

            if datetime.datetime(y, m, d).month == datetime.datetime.now().month:
                click.echo(date + ' ' + _time + ' ' +
                           currency_name + ' ' + number + ' ' + item)


def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        'status': status,
        'setup': setup,
        'exp': expense,
        'exps': expenses
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda money --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)
