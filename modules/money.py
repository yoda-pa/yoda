import click
import chalk
import os.path
import yaml
import config
from forex_python.converter import CurrencyRates, CurrencyCodes

# config file path
MONEY_CONFIG_FILE_PATH = os.environ.get('MONEY_CONFIG_FILE_PATH', config.MONEY_CONFIG_FILE_PATH)

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
    if not os.path.exists(os.path.dirname(MONEY_CONFIG_FILE_PATH)):
        try:
            os.makedirs(os.path.dirname(MONEY_CONFIG_FILE_PATH))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if os.path.isfile(MONEY_CONFIG_FILE_PATH):
        chalk.red('A configuration file already exists. Are you sure you want to overwrite it? (y/n)')
        overwrite_response = raw_input().lower()
        if not (overwrite_response == 'y' or overwrite_response == 'yes'):
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

    with open(MONEY_CONFIG_FILE_PATH, 'a') as config_file:
        yaml.dump(setup_data, config_file, default_flow_style=False)

# command checker
def check_sub_command(c):
    sub_commands = {
        'status' : status,
        'setup' : setup
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude setup --help" for more info')

# the main process
def process(input):
    input = input.lower().strip()
    check_sub_command(input)
