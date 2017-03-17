import click
import chalk
from config import config_file_paths
from util import *

# config file path
LOVE_CONFIG_FILE_PATH = config_file_paths["LOVE_CONFIG_FILE_PATH"]
LOVE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(LOVE_CONFIG_FILE_PATH)

# check status of setup
def status():
    if os.path.isfile(LOVE_CONFIG_FILE_PATH):
        with open(LOVE_CONFIG_FILE_PATH, 'r') as config_file:
            contents = yaml.load(config_file)
            click.echo(contents)
    else:
        chalk.red('The configuration file for this module does not exist. Please type "dude money setup" to create a new one')

def setup():
    create_folder(LOVE_CONFIG_FOLDER_PATH)

    if ask_overwrite(LOVE_CONFIG_FILE_PATH):
        return

    chalk.blue('Enter their name:')
    name = (raw_input().strip())

    chalk.blue('Where do they live?')
    place = (raw_input().strip())

    setup_data = dict (
        name = name,
        place = place
    )

    input_data(LOVE_CONFIG_FILE_PATH, setup_data)

def note():
    return

def reminder():
    return

# command checker
def check_sub_command(c):
    sub_commands = {
        'setup' : setup,
        'status' : status,
        'note' : note,
        'reminder' : reminder
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude setup --help" for more info')

def process(input):
    input = input.lower().strip()
    check_sub_command(input)
