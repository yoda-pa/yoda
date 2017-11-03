import click

from config import get_config_file_paths
from util import *

# config file path
LOVE_CONFIG_FILE_PATH = get_config_file_paths()["LOVE_CONFIG_FILE_PATH"]
LOVE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(LOVE_CONFIG_FILE_PATH)
LOVE_NOTES_FILE_PATH = LOVE_CONFIG_FOLDER_PATH + '/notes.yaml'


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents['notes'].append(
            data
        )

        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)


def status():
    """
    check status
    """
    if os.path.isfile(LOVE_CONFIG_FILE_PATH):
        with open(LOVE_CONFIG_FILE_PATH) as config_file:
            contents = yaml.load(config_file)
            click.echo(contents)
    else:
        chalk.red(
            'The configuration file for this module does not exist. Please type "yoda love setup" to create a new one')


def setup():
    """
    create new setup
    :return:
    """
    create_folder(LOVE_CONFIG_FOLDER_PATH)

    if ask_overwrite(LOVE_CONFIG_FILE_PATH):
        return

    chalk.blue('Enter their name:')
    name = (raw_input().strip())

    chalk.blue('Enter sex(M/F):')
    sex = (raw_input().strip())

    chalk.blue('Where do they live?')
    place = (raw_input().strip())

    setup_data = dict(
        name=name,
        place=place,
        sex=sex
    )

    input_data(setup_data, LOVE_CONFIG_FILE_PATH)


def note():
    """
    add a note for them
    """
    if os.path.isfile(LOVE_NOTES_FILE_PATH):
        data = dict(
            note=raw_input()
        )
        append_data_into_file(data, LOVE_NOTES_FILE_PATH)
    else:
        data = dict(
            notes=[
                dict(
                    note=raw_input()
                )
            ]
        )
        input_data(data, LOVE_NOTES_FILE_PATH)


def notes():
    """
    view notes
    """
    if os.path.isfile(LOVE_NOTES_FILE_PATH):
        with open(LOVE_NOTES_FILE_PATH, 'r') as notes_file:
            contents = yaml.load(notes_file)
            i = 0
            click.echo('Notes:')
            for n in contents['notes']:
                i += 1
                click.echo(str(i) + ": " + n['note'])
    else:
        chalk.red(
            'The configuration file for this module does not exist. Please type "yoda love setup" to create a new one')


def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        'setup': setup,
        'status': status,
        'note': note,
        'notes': notes
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "yoda love --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)
