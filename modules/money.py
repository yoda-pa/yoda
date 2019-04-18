from __future__ import absolute_import
from builtins import input
from builtins import map
import datetime
import json
import shlex
import time


from forex_python.converter import (
    CurrencyRates,
    CurrencyCodes,
    convert,
    RatesNotAvailableError,
)

from . import config
from .config import get_config_file_paths
from .util import *

CLIENT_ACCESS_TOKEN = os.environ.get("API_AI_TOKEN", config.API_AI_TOKEN)


# config file path
MONEY_CONFIG_FILE_PATH = get_config_file_paths()["MONEY_CONFIG_FILE_PATH"]
MONEY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(MONEY_CONFIG_FILE_PATH)

# currency converter
currency_rates = CurrencyRates()
currency_codes = CurrencyCodes()

# required to be compatible with mocking tests
request = None

'''
setup function for apiai import and related variables
Putting these in a function improves load time for all yoda commands
'''
def import_apiai():
    global apiai, request
    import apiai

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.session_id = os.environ.get("API_AI_SESSION_ID", config.API_AI_SESSION_ID)


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
    if (
        currency_name is None
        or len(currency_name) == 0
        or amount is None
        or len(amount) == 0
    ):
        return False
    else:
        return True


def status():
    """
    check status of setup
    """
    if os.path.isfile(MONEY_CONFIG_FILE_PATH):
        with open(MONEY_CONFIG_FILE_PATH) as config_file:
            contents = yaml.load(config_file)
            click.echo(contents)
    else:
        click.echo(
            'The configuration file for this module does not exist. Please type "yoda money setup" to create a new one'
        )


def setup():
    """
    create new setup config
    :return:
    """
    create_folder(MONEY_CONFIG_FOLDER_PATH)

    if ask_overwrite(MONEY_CONFIG_FILE_PATH):
        return

    click.echo(chalk.blue("Enter default currency code:"))
    currency_code = input().strip()
    click.echo(currency_rates.get_rates(currency_code))
    click.echo(currency_codes.get_symbol(currency_code))
    click.echo(currency_codes.get_currency_name(currency_code))

    click.echo(chalk.blue("Enter initial amount:"))
    initial_money = int(input().strip())

    setup_data = dict(currency_code=currency_code, initial_money=initial_money)

    input_data(setup_data, MONEY_CONFIG_FILE_PATH)


def expense():
    import_apiai()
    """
    add expense
    """
    create_folder(MONEY_CONFIG_FOLDER_PATH)
    with open(MONEY_CONFIG_FOLDER_PATH + "/expenditures.txt", "a") as fp:
        request.query = input()
        click.echo("output: ")
        response = request.getresponse().read()
        output = json.loads(response.decode('utf8').replace('\n', ''))
        # click.echo(output)
        currency_name = output["result"]["parameters"]["currency-name"]
        item = (
            output["result"]["parameters"]["any"]
            if len(output["result"]["parameters"]["any"].split()) == 1
            else ('"' + output["result"]["parameters"]["any"] + '"')
        )
        number = output["result"]["parameters"]["number"]

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        valid_expense = __validate_currency_name_and_amount(currency_name, number)
        if valid_expense == False:
            click.echo("Invalid Expense!")
        else:
            fp.write("{} {} {} {}\n".format(timestamp, currency_name, number, item))


def expenses():
    """
    check expenses
    """
    with open(MONEY_CONFIG_FOLDER_PATH + "/expenditures.txt") as fp:
        for line in fp.read().split("\n"):
            if len(line) == 0:
                continue
            (date, _time, currency_name, number, item) = shlex.split(line)
            y, m, d = list(map(int, date.split("-")))

            if datetime.datetime(y, m, d).month == datetime.datetime.now().month:
                click.echo(
                    date + " " + _time + " " + currency_name + " " + number + " " + item
                )


def expenses_month():
    """
    check expenses per month
    """

    tmp_dict = {}
    default_cur = None
    with open(MONEY_CONFIG_FOLDER_PATH + "/expenditures.txt") as fp:
        for line in fp.read().split("\n"):
            if len(line) == 0:
                continue
            (date, _time, currency_name, number, item) = shlex.split(line)
            y, m, d = list(map(int, date.split("-")))

            if m not in tmp_dict:
                tmp_dict[m] = float(number)
            else:
                tmp_dict[m] += float(number)

            default_cur = currency_name

        import calendar

        if len(tmp_dict) != 0:
            for k in tmp_dict:
                click.echo(
                    calendar.month_abbr[k]
                    + ": spent "
                    + str(tmp_dict[k])
                    + " "
                    + default_cur
                )


def convertCurrency():
    """
    Convert from one currency to other.
    """
    try:
        click.echo(chalk.blue("Enter currency codes seperated by space:"))
        currency_name_from, currency_name_to = input().split()
        currency_rate_per_unit = currency_rates.get_rates(currency_name_from)[
            currency_name_to
        ]
        click.echo(
            currency_codes.get_symbol(currency_name_from)
            + " 1"
            + " = "
            + currency_codes.get_symbol(currency_name_to)
            + " "
            + str(currency_rate_per_unit)
        )
        click.echo(
            "Enter the amount in "
            + currency_name_from
            + " to be converted to "
            + currency_name_to
        )
        currency_amount_to_be_converted = int(input())
        converted_amount = convert(
            currency_name_from, currency_name_to, currency_amount_to_be_converted
        )
        click.echo(
            str(currency_amount_to_be_converted)
            + " "
            + currency_name_from
            + " = "
            + str(converted_amount)
            + " "
            + currency_name_to
        )
    except RatesNotAvailableError:
        click.echo(
            chalk.red("Currency code does not exist. Try with some other currency code")
        )
    except:
        click.echo(chalk.red("Something went wrong. Try again!"))


def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        "status": status,
        "setup": setup,
        "exp": expense,
        "exps": expenses,
        "exps_month": expenses_month,
        "convert": convertCurrency,
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
        click.echo('Try "yoda money --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)
