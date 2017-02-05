import click
import chalk
import config
import os.path
import time
import yaml

# config file path
DIARY_CONFIG_FILE_PATH = os.environ.get('DIARY_CONFIG_FILE_PATH', config.DIARY_CONFIG_FILE_PATH)

# get time
def now_time():
    return str(time.strftime("%H:%M:%S"))

# get date
def now_date():
    return str(time.strftime("%d-%m-%Y"))

# get file path for today's tasks entry file
def todays_tasks_entry_file_path():
    return os.path.dirname(DIARY_CONFIG_FILE_PATH) + '/' + now_date() + "-tasks.yaml"

# get file path for today's notes entry file
def todays_notes_entry_file_path():
    return os.path.dirname(DIARY_CONFIG_FILE_PATH) + '/' + now_date() + "-notes.yaml"

# check if today's diary entry file exists. If not, create
def today_entry_check():
    if not os.path.exists(os.path.dirname(DIARY_CONFIG_FILE_PATH)):
        try:
            os.makedirs(os.path.dirname(DIARY_CONFIG_FILE_PATH))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

# new journal entry
# operations: new task, task complete, task postponed, take notes
def new_task():
    today_entry_check()
    with open(todays_tasks_entry_file_path(), "a") as todays_tasks_entry:
        todays_tasks_entry.write("appended text")

def new_note():
    today_entry_check()

    chalk.blue('Input your entry:')
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
    click.echo('Today\'s agenda:')
    if os.path.isfile(todays_notes_entry_file_path()):
        with open(todays_notes_entry_file_path(), 'r') as config_file:
            contents = yaml.load(config_file)
            # TODO: beautify output
            click.echo(contents)
    else:
        click.echo('The configuration file for this module does not exist. Please type "dude money setup" to create a new one')

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
