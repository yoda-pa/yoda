import click
import chalk
from config import config_file_paths
import os.path
import time
import yaml
from util import *

# config file path
DIARY_CONFIG_FILE_PATH = config_file_paths['DIARY_CONFIG_FILE_PATH']
DIARY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(DIARY_CONFIG_FILE_PATH)

# get time
def now_time():
    return str(time.strftime("%H:%M:%S"))

# get date
def now_date():
    return str(time.strftime("%d-%m-%Y"))

# get file path for today's tasks entry file
def todays_tasks_entry_file_path():
    return DIARY_CONFIG_FOLDER_PATH + '/' + now_date() + "-tasks.yaml"

# get file path for today's notes entry file
def todays_notes_entry_file_path():
    return DIARY_CONFIG_FOLDER_PATH + '/' + now_date() + "-notes.yaml"

# check if today's diary entry file exists. If not, create
def today_entry_check():
    if not os.path.exists(DIARY_CONFIG_FOLDER_PATH):
        try:
            os.makedirs(DIARY_CONFIG_FOLDER_PATH)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

# new journal entry
# operations: new task, task complete, task postponed, take notes
def new_task():
    today_entry_check()

    chalk.blue('Input your entry for task:')
    note = raw_input().strip()

    if os.path.isfile(todays_tasks_entry_file_path()):
        with open(todays_tasks_entry_file_path(), "r") as todays_tasks_entry:

            contents = yaml.load(todays_tasks_entry)
            contents['entries'].append(
                dict(
                    time = now_time(),
                    text = note
                )
            )

            with open(todays_tasks_entry_file_path(), "w") as todays_tasks_entry:
                yaml.dump(contents, todays_tasks_entry, default_flow_style=False)
    else:
        with open(todays_tasks_entry_file_path(), "w") as todays_tasks_entry:
            setup_data = dict (
                entries = [
                    dict(
                        time = now_time(),
                        text = note
                    )
                ]
            )
            yaml.dump(setup_data, todays_tasks_entry, default_flow_style=False)


def new_note():
    today_entry_check()

    chalk.blue('Input your entry for note:')
    note = raw_input().strip()

    if os.path.isfile(todays_notes_entry_file_path()):
        with open(todays_notes_entry_file_path(), "r") as todays_notes_entry:

            contents = yaml.load(todays_notes_entry)
            contents['entries'].append(
                dict(
                    time = now_time(),
                    text = note
                )
            )

            with open(todays_notes_entry_file_path(), "w") as new_todays_notes_entry:
                yaml.dump(contents, new_todays_notes_entry, default_flow_style=False)
    else:
        with open(todays_notes_entry_file_path(), "w") as todays_notes_entry:
            setup_data = dict (
                entries = [
                    dict(
                        time = now_time(),
                        text = note
                    )
                ]
            )
            yaml.dump(setup_data, todays_notes_entry, default_flow_style=False)

def agenda():
    if os.path.isfile(todays_notes_entry_file_path()):
        click.echo('Today\'s agenda:')
        with open(todays_notes_entry_file_path(), 'r') as config_file:
            contents = yaml.load(config_file)
            # TODO: beautify output
            click.echo(contents)
    else:
        click.echo('There is no agenda for today. Add a new task by entering "dude nt *task*"')

# command checker
def check_sub_command(c):
    sub_commands = {
        'agenda' : agenda,
        'nn' : new_note,
        'nt' : new_task
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
