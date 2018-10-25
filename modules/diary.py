from __future__ import absolute_import
from builtins import input
from builtins import str
from builtins import range
import calendar
import datetime
import os.path
import time
from os import listdir

from .goals import add_task_to_goal

from .config import get_config_file_paths
from .util import *

# config file path
DIARY_CONFIG_FILE_PATH = get_config_file_paths()["DIARY_CONFIG_FILE_PATH"]
DIARY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(DIARY_CONFIG_FILE_PATH)


def now_time():
    """
    get time
    :return:
    """
    return str(time.strftime("%H:%M:%S"))


def now_date():
    """
    get date
    :return:
    """
    return str(time.strftime("%d-%m-%Y"))


def yesterdays_date():
    """
    get yesterday's date
    """
    yesterday = datetime.date.today() - datetime.timedelta(1)
    return str(yesterday.strftime("%d-%m-%Y"))


def todays_tasks_entry_file_path():
    """
    get file path for today's tasks entry file
    :return:
    """
    return DIARY_CONFIG_FOLDER_PATH + "/" + now_date() + "-tasks.yaml"


def todays_notes_entry_file_path():
    """
    get file path for today's notes entry file
    :return:
    """
    return DIARY_CONFIG_FOLDER_PATH + "/" + now_date() + "-notes.yaml"


def yesterdays_notes_entry_file_path():
    """
    get file path for yesterday's notes entry file
    """
    return DIARY_CONFIG_FOLDER_PATH + "/" + yesterdays_date() + "-notes.yaml"


def yesterdays_tasks_entry_file_path():
    """
    get file path for yesterday's tasks entry file
    """

    return DIARY_CONFIG_FOLDER_PATH + "/" + yesterdays_date() + "-tasks.yaml"


def tasks_entry_file_path(date):
    """
    get file path for the specified date's notes entry file
    """
    return DIARY_CONFIG_FOLDER_PATH + "/" + date + "-tasks.yaml"


TODAYS_TASKS_ENTRY_FILE_PATH = todays_tasks_entry_file_path()
TODAYS_NOTES_ENTRY_FILE_PATH = todays_notes_entry_file_path()

YESTERDAYS_TASKS_ENTRY_FILE_PATH = yesterdays_tasks_entry_file_path()
YESTERDAYS_NOTES_ENTRY_FILE_PATH = yesterdays_notes_entry_file_path()


def today_entry_check():
    """
    check if today's diary entry file exists. If not, create
    """
    if not os.path.exists(DIARY_CONFIG_FOLDER_PATH):
        try:
            os.makedirs(DIARY_CONFIG_FOLDER_PATH)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents["entries"].append(data)

        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)


# new journal entry
# operations: new task, task complete, task postponed, take notes


def new_task():
    """
    new task
    """
    today_entry_check()

    click.echo(chalk.blue("Input your entry for task:"))
    note = input().strip()

    timestamp = now_time()
    date = now_date()

    hashtags = []
    continue_adding_hashtags = True

    while continue_adding_hashtags:
        click.echo(
            chalk.blue(
                "Enter the name of the goal that you would like to associate task with or -"
            )
        )
        hashtag = input().strip()

        if hashtag == "-":
            continue_adding_hashtags = False
        else:
            if add_task_to_goal(hashtag, date, timestamp):
                click.echo(chalk.green("Task added to the goal"))
                hashtags.append("#" + hashtag)
            else:
                click.echo(chalk.red("Invalid goal name"))

    if os.path.isfile(TODAYS_TASKS_ENTRY_FILE_PATH):
        setup_data = dict(
            time=timestamp, text=note, status=0, hashtags=" ".join(hashtags)
        )
        append_data_into_file(setup_data, TODAYS_TASKS_ENTRY_FILE_PATH)
    else:
        setup_data = dict(
            entries=[
                dict(time=timestamp, text=note, status=0, hashtags=" ".join(hashtags))
            ]
        )
        input_data(setup_data, TODAYS_TASKS_ENTRY_FILE_PATH)


def new_note():
    """
    new note
    """
    today_entry_check()

    click.echo(chalk.blue("Input your title for note:"))
    note_title = input().strip()

    click.echo(chalk.blue("Input your text for note:"))
    note_text = input().strip()

    if os.path.isfile(TODAYS_NOTES_ENTRY_FILE_PATH):
        with open(TODAYS_NOTES_ENTRY_FILE_PATH) as todays_notes_entry:
            setup_data = dict(time=now_time(), title=note_title, text=note_text)
            append_data_into_file(setup_data, TODAYS_NOTES_ENTRY_FILE_PATH)
    else:
        setup_data = dict(
            entries=[dict(time=now_time(), title=note_title, text=note_text)]
        )
        input_data(setup_data, TODAYS_NOTES_ENTRY_FILE_PATH)


def strike(text):
    """
    strikethrough text
    :param text:
    :return:
    """
    return u"\u0336".join(text) + u"\u0336"


def tasks(today=True):
    """
    get tasks
    """

    if today == True:
        file_path = TODAYS_TASKS_ENTRY_FILE_PATH
        day_string = "Today"
    else:
        file_path = YESTERDAYS_TASKS_ENTRY_FILE_PATH
        day_string = "Yesterday"

    if os.path.isfile(file_path):
        click.echo(day_string + "'s" + " agenda:")
        click.echo("----------------")
        click.echo("Status |  Time   | Text")
        click.echo("-------|---------|-----")
        incomplete_tasks = 0
        total_tasks = 0
        with open(file_path) as todays_tasks_entry:
            contents = yaml.load(todays_tasks_entry)
            for entry in contents["entries"]:
                total_tasks += 1
                incomplete_tasks += 1 if entry["status"] == 0 else 0
                time = entry["time"]
                text = entry["text"] + " " + entry.get("hashtags", "")
                text = text if entry["status"] == 0 else strike(text)
                status = "O" if entry["status"] == 0 else "X"
                click.echo("   " + status + "   | " + time + ": " + text)
        click.echo("----------------")
        click.echo("")
        click.echo("Summary:")
        click.echo("----------------")
        if incomplete_tasks == 0:
            click.echo(
                chalk.green(
                    'All tasks have been competed! Add a new task by entering "yoda  diary nt"'
                )
            )
        else:
            click.echo(chalk.red("Incomplete tasks: " + str(incomplete_tasks)))
            click.echo(
                chalk.green("Completed tasks: " + str(total_tasks - incomplete_tasks))
            )

    else:
        click.echo("There are no tasks for " + day_string.lower() + ".")
        if today == True:
            click.echo('Add a new task by entering "yoda diary nt"')


def complete_task():
    """
    complete a task
    """
    not_valid_task_number = 1
    if os.path.isfile(TODAYS_TASKS_ENTRY_FILE_PATH):
        with open(TODAYS_TASKS_ENTRY_FILE_PATH) as todays_tasks_entry:
            contents = yaml.load(todays_tasks_entry)
            no_task_left = True
            for i, entry in enumerate(contents["entries"]):
                if entry["status"] == 0:
                    no_task_left = False

            if no_task_left:
                click.echo(
                    chalk.green(
                        'All tasks have been competed! Add a new task by entering "yoda  diary nt"'
                    )
                )
            else:
                click.echo("Today's agenda:")
                click.echo("----------------")
                click.echo("Number |  Time   | Task")
                click.echo("-------|---------|-----")

                for i, entry in enumerate(contents["entries"]):
                    time = entry["time"]
                    text = entry["text"] + " " + entry.get("hashtags", "")
                    text = text if entry["status"] == 0 else strike(text)
                    if entry["status"] == 0:
                        click.echo("   " + str(i) + "   | " + time + ": " + text)
                while not_valid_task_number:
                    click.echo(
                        chalk.blue(
                            "Enter the task number that you would like to set as completed"
                        )
                    )
                    task_to_be_completed = int(input())
                    if task_to_be_completed > len(contents["entries"]):
                        click.echo(chalk.red("Please Enter a valid task number!"))
                    else:
                        contents["entries"][task_to_be_completed - 1]["status"] = 1
                        input_data(contents, TODAYS_TASKS_ENTRY_FILE_PATH)
                        not_valid_task_number = 0
    else:
        click.echo(
            chalk.red(
                'There are no tasks for today. Add a new task by entering "yoda diary nt"'
            )
        )


def delete_task():
    """
	delete a particular task
	"""
    list_of_files = list_of_tasks_files()
    if list_of_files:
        not_valid_task_number = 1
        not_valid_date_number = 1
        click.echo("Select the date:- \n")
        click.echo("--------------------")
        click.echo("Number |    Date    ")
        click.echo("--------------------")
        for i, some_file in enumerate(range(0, len(list_of_files))):
            click.echo(str(i) + "      |" + list_of_files[some_file][0:10])
        while not_valid_date_number:
            click.echo(chalk.blue("Enter the number to select the date"))
            selected_date = int(input())
            if selected_date > len(list_of_files):
                click.echo(chalk.red("Please Enter a valid task number!"))
            else:
                SELECTED_DATE_PATH = os.path.join(
                    DIARY_CONFIG_FOLDER_PATH + "/" + list_of_files[selected_date - 1]
                )
                with open(SELECTED_DATE_PATH) as selected_task:
                    contents = yaml.load(selected_task)
                    click.echo("\nTasks for " + list_of_files[some_file][0:10])
                    click.echo("----------------")
                    click.echo("Number |  Time   | Task")
                    click.echo("-------|---------|-----")
                    for i, entry in enumerate(contents["entries"]):
                        time = entry["time"]
                        text = entry["text"] + " " + entry.get("hashtags", "")
                        text = text if entry["status"] == 0 else strike(text)
                        click.echo("   " + str(i) + "   | " + time + ": " + text)
                not_valid_date_number = 0
        while not_valid_task_number:
            click.echo(
                chalk.blue("Enter the task number that you would like to delete")
            )
            task_to_be_deleted = int(input())
            if task_to_be_deleted > len(contents["entries"]):
                click.echo(chalk.red("Please Enter a valid task number!"))
            else:
                del contents["entries"][task_to_be_deleted - 1]
                input_data(contents, SELECTED_DATE_PATH)
                not_valid_task_number = 0
    else:
        click.echo(
            chalk.red('There are no tasks. Add a new task by entering "yoda diary nt"')
        )


def delete_note():

    """
delete a particular note
	"""
    list_of_files = list_of_notes_files()
    if list_of_files:
        not_valid_note_number = 1
        not_valid_date_number = 1
        click.echo("Select the date:- \n")
        click.echo("--------------------")
        click.echo("Number |    Date    ")
        click.echo("--------------------")
        for i, some_file in enumerate(range(0, len(list_of_files))):
            click.echo(str(i) + "      |" + list_of_files[some_file][0:10])
        while not_valid_date_number:
            click.echo(chalk.blue("Enter the number to select the date"))
            selected_date = int(input())
            if selected_date > len(list_of_files):
                click.echo(chalk.red("Please Enter a valid Date number!"))
            else:
                SELECTED_DATE_PATH = os.path.join(
                    DIARY_CONFIG_FOLDER_PATH + "/" + list_of_files[selected_date - 1]
                )
                with open(SELECTED_DATE_PATH) as selected_note:
                    contents = yaml.load(selected_note)
                    click.echo("\nNotes for " + list_of_files[some_file][0:10])
                    click.echo("----------------")
                    click.echo("Number |  Time   |   Title    | Text")
                    click.echo("-------|---------|------------|-----")
                    for i, entry in enumerate(contents["entries"]):
                        time = entry["time"]
                        note_title = entry["title"]
                        text = entry["text"]
                        click.echo(
                            str(i)
                            + "      |"
                            + time
                            + " |  "
                            + note_title
                            + "  | "
                            + text
                        )
                not_valid_date_number = 0
        while not_valid_note_number:
            click.echo(
                chalk.blue("Enter the note number that you would like to delete")
            )
            note_to_be_deleted = int(input())
            if note_to_be_deleted > len(contents["entries"]):
                click.echo(chalk.red("Please Enter a valid note number!"))
            else:
                del contents["entries"][note_to_be_deleted - 1]
                input_data(contents, SELECTED_DATE_PATH)
                not_valid_note_number = 0
                if len(contents["entries"]) == 0:
                    os.remove(SELECTED_DATE_PATH)
    else:
        click.echo(
            chalk.red('There are no tasks. Add a new task by entering "yoda diary nt"')
        )


def notes(today=True):
    """
    see notes for today
    """

    if today == True:
        file_path = TODAYS_NOTES_ENTRY_FILE_PATH
        day_string = "Today"
    else:
        file_path = YESTERDAYS_NOTES_ENTRY_FILE_PATH
        day_string = "Yesterday"

    if os.path.isfile(file_path):
        with open(file_path) as todays_notes_entry:
            contents = yaml.load(todays_notes_entry)

            click.echo(day_string + "'s notes:")
            click.echo("----------------")
            click.echo("  Time  |  Title  |	Note ")
            click.echo("--------|---------|------")

            for entry in contents["entries"]:
                time = entry["time"]
                note_title = entry["title"]
                text = entry["text"]
                click.echo(time + "|  " + note_title + "  | " + text)

    else:
        click.echo(chalk.red("There are no notes for " + day_string.lower() + "."))
        if today == True:
            click.echo('Add a new note by entering "yoda diary nn"')


def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        "tasks": tasks,
        "nn": new_note,
        "nt": new_task,
        "ct": complete_task,
        "dt": delete_task,
        "dn": delete_note,
        "un": update_note,
        "ut": update_task,
        "dct": delete_completed_task,
        "notes": notes,
        "analyze": current_month_task_analysis,
    }

    c = c.split(" ")

    try:
        if len(c) == 1:
            return sub_commands[c[0]]()
        elif len(c) == 2 and (c[0] == "tasks" or c[0] == "notes"):
            return sub_commands[c[0]](False)
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
        click.echo('Try "yoda diary --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)


def list_of_notes_files():
    """
    list of all notes files
    :return:
    """
    current_month = time.strftime("%m")
    current_year = time.strftime("%Y")
    files = [
        f
        for f in listdir(DIARY_CONFIG_FOLDER_PATH)
        if os.path.isfile(os.path.join(DIARY_CONFIG_FOLDER_PATH, f))
    ]
    list_of_files = []
    for i in files:
        x = i[3:16].split("-")
        if x[0] == current_month and x[1] == current_year and x[2] == "notes":
            list_of_files.append(i)
    return list_of_files


def list_of_tasks_files():
    """
    list of all tasks files
    :return:def update_note():
	list_of_files = list_of_notes_files()
	if list_of_files:
		not_valid_note_number = 1
		not_valid_date_number = 1
		click.echo('Select the date:- \n')
		click.echo('--------------------')
		click.echo('Number |    Date    ')
		click.echo('--------------------')
		for i, some_file in enumerate(range(0, len(list_of_files))):
			click.echo(str(i)+'      |'+list_of_files[some_file][0:10])
		while not_valid_date_number:
			click.echo(chalk.blue('Enter the number to select the date'))
			selected_date=int(input())
			if selected_date > len(list_of_files):
				click.echo(chalk.red('Please Enter a valid Date number!'))
			else:
				SELECTED_DATE_PATH=os.path.join(DIARY_CONFIG_FOLDER_PATH+'/'+list_of_files[selected_date-1])
				with open(SELECTED_DATE_PATH) as selected_note:
					contents = yaml.load(selected_note)
					click.echo('\nNotes for '+list_of_files[some_file][0:10])
					click.echo('------------------------------------')
					click.echo("Number |  Time   |   Title    | Text")
					click.echo("-------|---------|------------|-----")
					for i, entry in enumerate(contents['entries']):
						time = entry['time']
						note_title=entry['title']
						text = entry['text']
						click.echo(str(i)+'      |'+time + " |  " + note_title +"  | "+text)
				not_valid_date_number=0
		while not_valid_note_number:
			click.echo(chalk.blue('Enter the note number that you would like to update'))
			note_to_be_deleted = int(input())
			if note_to_be_deleted > len(contents['entries']):
				click.echo(chalk.red('Please Enter a valid note number!'))
			else:
				not_valid_note_number=0
				click.echo(chalk.blue('Enter the new text'))
				new_note=input()
                contents['entries'][note_to_be_deleted - 1]['text']=new_note
                input_data(contents, TODAYS_NOTES_ENTRY_FILE_PATH)
                
	else:
		click.echo(chalk.red(
            'There are no tasks. Add a new task by entering "yoda diary nt"'))
    """
    current_month = time.strftime("%m")
    current_year = time.strftime("%Y")
    files = [
        f
        for f in listdir(DIARY_CONFIG_FOLDER_PATH)
        if os.path.isfile(os.path.join(DIARY_CONFIG_FOLDER_PATH, f))
    ]
    list_of_files = []
    for i in files:
        x = i[3:16].split("-")
        if x[0] == current_month and x[1] == current_year and x[2] == "tasks":
            list_of_files.append(i)
    return list_of_files


def current_month_task_analysis():
    """
    current month task analysis
    """
    now = datetime.datetime.now()
    no_of_days_current_month = calendar.monthrange(now.year, now.month)[1]
    total_tasks = 0
    total_incomplete_tasks = 0
    list_of_files = list_of_tasks_files()
    for some_file in range(0, len(list_of_files)):
        list_of_files[some_file] = os.path.join(
            DIARY_CONFIG_FOLDER_PATH, list_of_files[some_file]
        )
    for some_file in list_of_files:
        with open(some_file) as fp:
            contents = yaml.load(fp)
            for entry in contents["entries"]:
                total_tasks += 1
                total_incomplete_tasks += 1 if entry["status"] == 0 else 0

    if total_tasks:
        percent_incomplete_task = total_incomplete_tasks * 100 / total_tasks
        percent_complete_task = 100 - percent_incomplete_task
        entry_frequency = total_tasks * 100 / no_of_days_current_month
        click.echo(
            chalk.red("Percentage of incomplete task : " + str(percent_incomplete_task))
        )
        click.echo(
            chalk.green("Percentage of complete task : " + str(percent_complete_task))
        )
        click.echo(
            chalk.blue("Frequency of adding task (Task/Day) : " + str(entry_frequency))
        )
    else:
        click.echo(
            'There are no tasks for this month. Add a new task by entering "yoda diary nt"'
        )


def get_task_info(timestamp, date):
    filename = tasks_entry_file_path(date)
    if os.path.isfile(filename):
        with open(filename) as file:
            contents = yaml.load(file)
            for entry in contents["entries"]:
                if entry["time"] == timestamp:
                    return entry["status"], entry["text"]
    return None


def update_task():
    """
update a particular task
	"""

    list_of_files = list_of_tasks_files()
    if list_of_files:
        not_valid_task_number = 1
        not_valid_date_number = 1
        click.echo("Select the date:- \n")
        click.echo("--------------------")
        click.echo("Number |    Date    ")
        click.echo("--------------------")
        for i, some_file in enumerate(range(0, len(list_of_files))):
            click.echo(str(i) + "      |" + list_of_files[some_file][0:10])
        while not_valid_date_number:
            click.echo(chalk.blue("Enter the number to select the date"))
            selected_date = int(input())
            if selected_date > len(list_of_files):
                click.echo(chalk.red("Please Enter a valid date number!"))
            else:
                SELECTED_DATE_PATH = os.path.join(
                    DIARY_CONFIG_FOLDER_PATH + "/" + list_of_files[selected_date - 1]
                )
                with open(SELECTED_DATE_PATH) as selected_task:
                    contents = yaml.load(selected_task)
                    click.echo("\nTasks for " + list_of_files[some_file][0:10])
                    click.echo("-----------------------")
                    click.echo("Number |  Time   | Task")
                    click.echo("-------|---------|-----")
                    for i, entry in enumerate(contents["entries"]):
                        time = entry["time"]
                        text = entry["text"] + " " + entry.get("hashtags", "")
                        text = text if entry["status"] == 0 else strike(text)
                        click.echo("   " + str(i) + "   | " + time + ": " + text)
                not_valid_date_number = 0
        while not_valid_task_number:
            click.echo(
                chalk.blue("Enter the task number that you would like to update")
            )
            task_to_be_updated = int(input())
            if task_to_be_updated > len(contents["entries"]):
                click.echo(chalk.red("Please Enter a valid task number!"))
            else:
                click.echo(chalk.blue("Enter the new task"))
                not_valid_task_number = 0
                new_text = str(input())
                contents["entries"][task_to_be_updated - 1]["text"] = new_text
                input_data(contents, TODAYS_TASKS_ENTRY_FILE_PATH)
    else:
        click.echo(
            chalk.red('There are no tasks. Add a new task by entering "yoda diary nt"')
        )


def update_note():

    """
	update a particular note
	"""
    list_of_files = list_of_notes_files()
    if list_of_files:
        not_valid_note_number = 1
        not_valid_date_number = 1
        click.echo("Select the date:- \n")
        click.echo("--------------------")
        click.echo("Number |    Date    ")
        click.echo("--------------------")
        for i, some_file in enumerate(range(0, len(list_of_files))):
            click.echo(str(i) + "      |" + list_of_files[some_file][0:10])
        while not_valid_date_number:
            click.echo(chalk.blue("Enter the number to select the date"))
            selected_date = int(input())
            if selected_date > len(list_of_files):
                click.echo(chalk.red("Please Enter a valid Date number!"))
            else:
                SELECTED_DATE_PATH = os.path.join(
                    DIARY_CONFIG_FOLDER_PATH + "/" + list_of_files[selected_date - 1]
                )
                with open(SELECTED_DATE_PATH) as selected_note:
                    contents = yaml.load(selected_note)
                    click.echo("\nNotes for " + list_of_files[some_file][0:10])
                    click.echo("------------------------------------")
                    click.echo("Number |  Time   |   Title    | Text")
                    click.echo("-------|---------|------------|-----")
                    for i, entry in enumerate(contents["entries"]):
                        time = entry["time"]
                        note_title = entry["title"]
                        text = entry["text"]
                        click.echo(
                            str(i)
                            + "      |"
                            + time
                            + " |  "
                            + note_title
                            + "  | "
                            + text
                        )
                not_valid_date_number = 0
        while not_valid_note_number:
            click.echo(
                chalk.blue("Enter the note number that you would like to update")
            )
            note_to_be_updated = int(input())
            if note_to_be_updated > len(contents["entries"]):
                click.echo(chalk.red("Please Enter a valid note number!"))
            else:
                not_valid_note_number = 0
                click.echo(chalk.blue("Enter the new text"))
                new_note = input()
                contents["entries"][note_to_be_updated - 1]["text"] = new_note
                input_data(contents, TODAYS_NOTES_ENTRY_FILE_PATH)

    else:
        click.echo(
            chalk.red('There are no tasks. Add a new task by entering "yoda diary nt"')
        )


def delete_completed_task():
    """
	delete completed task
	"""
    not_valid_task_number = 1
    if os.path.isfile(TODAYS_TASKS_ENTRY_FILE_PATH):
        with open(TODAYS_TASKS_ENTRY_FILE_PATH) as todays_tasks_entry:
            contents = yaml.load(todays_tasks_entry)
            no_task_complete = None
            i = 0
            for entry in contents["entries"]:
                if entry["status"] == 1:
                    i += 1

            if i == 0:
                click.echo(
                    chalk.green(
                        'All tasks are incomplete! Complete a task by entering "yoda diary ct"'
                    )
                )
            else:
                click.echo("Today's agenda:")
                click.echo("----------------")
                click.echo("Number |  Time   | Task")
                click.echo("-------|---------|-----")
                for i, entry in enumerate(contents["entries"]):
                    time = entry["time"]
                    text = entry["text"] + " " + entry.get("hashtags", "")
                    text = text if entry["status"] == 0 else strike(text)
                    click.echo("   " + str(i) + "   | " + time + ": " + text)
                click.echo(chalk.blue("Type c to confirm or Ctrl-c to exit."))
                user_response = input()
                if user_response == "c":
                    for i, entry in enumerate(contents["entries"]):
                        if entry["status"] != 0:
                            del contents["entries"][i - 1]
                            input_data(contents, TODAYS_TASKS_ENTRY_FILE_PATH)

                else:
                    click.echo("Click c to confirm or Ctrl-C to exit")

    else:
        click.echo(
            chalk.red(
                'There are no tasks for today. Add a new task by entering "yoda diary nt"'
            )
        )
