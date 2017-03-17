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

# append data into existing file
def append_data_into_file(data, file_path):
    with open(file_path, "r") as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents['entries'].append(
            data
        )

        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)

# new journal entry
# operations: new task, task complete, task postponed, take notes
def new_task():
    today_entry_check()

    chalk.blue('Input your entry for task:')
    note = raw_input().strip()

    if os.path.isfile(todays_tasks_entry_file_path()):
        setup_data = dict(
            time = now_time(),
            text = note,
            status = 0
        )
        append_data_into_file(setup_data, todays_tasks_entry_file_path())
    else:
        setup_data = dict (
            entries = [
                dict(
                    time = now_time(),
                    text = note,
                    status = 0
                )
            ]
        )
        input_data(setup_data, todays_tasks_entry_file_path())

def new_note():
    today_entry_check()

    chalk.blue('Input your entry for note:')
    note = raw_input().strip()

    if os.path.isfile(todays_notes_entry_file_path()):
        with open(todays_notes_entry_file_path(), "r") as todays_notes_entry:
            setup_data = dict(
                time = now_time(),
                text = note
            )
            append_data_into_file(setup_data, todays_notes_entry_file_path())
    else:
        setup_data = dict (
            entries = [
                dict(
                    time = now_time(),
                    text = note
                )
            ]
        )
        input_data(setup_data, todays_notes_entry_file_path())


def strike(text):
    return u'\u0336'.join(text) + u'\u0336'

def agenda():
    if os.path.isfile(todays_tasks_entry_file_path()):
        click.echo('Today\'s agenda:')
        click.echo('----------------')
        click.echo("Status |  Time   | Text")
        click.echo("-------|---------|-----")
        incomplete_tasks = 0
        total_tasks = 0
        with open(todays_tasks_entry_file_path(), 'r') as todays_tasks_entry:
            contents = yaml.load(todays_tasks_entry)
            for entry in contents['entries']:
                total_tasks += 1
                incomplete_tasks += (1 if entry['status'] == 0 else 0)
                time = entry['time']
                text = entry['text'] if entry['status'] == 0 else strike(entry['text'])
                status = "O" if entry['status'] == 0 else "X"
                click.echo("   " + status + "   | " + time + ": " + text)
        click.echo('----------------')
        click.echo('')
        click.echo('Summary:')
        click.echo('----------------')
        if incomplete_tasks == 0:
            chalk.green('All tasks have been competed! Add a new task by entering "dude  diary nt"')
        else:
            chalk.red("Incomplete tasks: " + str(incomplete_tasks))
            chalk.green("Completed tasks: " + str(total_tasks - incomplete_tasks))

    else:
        click.echo('There is no agenda for today. Add a new task by entering "dude diary nt"')

def complete_task():
    if os.path.isfile(todays_tasks_entry_file_path()):
        with open(todays_tasks_entry_file_path(), 'r') as todays_tasks_entry:
            contents = yaml.load(todays_tasks_entry)
            i = 0
            no_task_left = True
            for entry in contents['entries']:
                i += 1
                if entry['status'] == 0:
                    no_task_left = False

            if no_task_left:
                chalk.green('All tasks have been competed! Add a new task by entering "dude  diary nt"')
            else:
                click.echo('Today\'s agenda:')
                click.echo('----------------')
                click.echo("Number |  Time   | Text")
                click.echo("-------|---------|-----")

                i = 0
                for entry in contents['entries']:
                    i += 1
                    time = entry['time']
                    text = entry['text'] if entry['status'] == 0 else strike(entry['text'])
                    status = "O" if entry['status'] == 0 else "X"
                    if entry['status'] == 0:
                        no_task_left = False
                        click.echo("   " + str(i) + "   | " + time + ": " + text)

                chalk.blue('Enter the task number that you would like to set as completed')
                task_to_be_completed = int(raw_input())
                contents['entries'][task_to_be_completed - 1]['status'] = 1
                input_data(contents, todays_tasks_entry_file_path())
    else:
        click.echo('There is no agenda for today. Add a new task by entering "dude nt *task*"')

# command checker
def check_sub_command(c):
    sub_commands = {
        'agenda' : agenda,
        'nn' : new_note,
        'nt' : new_task,
        'ct' : complete_task
    }
    # try:
    #     return sub_commands[c]()
    # except KeyError:
    #     chalk.red('Command does not exist!')
    #     click.echo('Try "dude setup --help" for more info')
    return sub_commands[c]()

# the main process
def process(input):
    input = input.lower().strip()
    check_sub_command(input)
