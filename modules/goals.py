from __future__ import absolute_import

import datetime

from .config import get_config_file_paths
from .util import *

# config file path
GOALS_CONFIG_FILE_PATH = get_config_file_paths()['GOALS_CONFIG_FILE_PATH']
GOALS_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    GOALS_CONFIG_FILE_PATH)


def strike(text):
    """
    strikethrough text
    :param text:
    :return:
    """
    return u'\u0336'.join(text) + u'\u0336'

def get_goal_file_path(goal_name):
    return GOALS_CONFIG_FOLDER_PATH + '/' + goal_name + '.yaml'

def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)

def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        'new': new_goal,
        'tasks': view_related_tasks,
        'view': list_goals,
        'complete': complete_goal,
        'analyze': goals_analysis,
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda goals --help" for more info')

def goals_dir_check():
    """
    check if goals directory exists. If not, create
    """
    if not os.path.exists(GOALS_CONFIG_FOLDER_PATH):
        try:
            os.makedirs(GOALS_CONFIG_FOLDER_PATH)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as file:
        # read contents
        contents = yaml.load(file)
        contents['entries'].append(
            data
        )

        # enter data
        with open(file_path, "w") as file:
            yaml.dump(contents, file, default_flow_style=False)

def complete_goal():
    """
    complete a goal
    """
    not_valid_goal_number = 1
    if os.path.isfile(GOALS_CONFIG_FILE_PATH):
        with open(GOALS_CONFIG_FILE_PATH) as todays_tasks_entry:
            contents = yaml.load(todays_tasks_entry)
            i = 0
            no_goal_left = True
            for entry in contents['entries']:
                i += 1
                if entry['status'] == 0:
                    no_goal_left = False

            if no_goal_left:
                click.echo(chalk.green(
                    'All goals have been completed! Add a new goal by entering "yoda goals new"'))
            else:
                click.echo('Goals:')
                click.echo('----------------')
                click.echo("Number |  Deadline   | Goal")
                click.echo("-------|-------------|-----")

                i = 0
                for entry in contents['entries']:
                    i += 1
                    deadline = entry['deadline']
                    text = entry['text'] if entry['status'] == 0 else strike(
                        entry['text'])
                    if entry['status'] == 0:
                        click.echo("   " + str(i) + "   | " +
                                   deadline + "  | " + text)
                while not_valid_goal_number:
                    click.echo(chalk.blue(
                        'Enter the goal number that you would like to set as completed'))
                    goal_to_be_completed = int(input())
                    if goal_to_be_completed > len(contents['entries']):
                        click.echo(chalk.red('Please Enter a valid goal number!'))
                    else:
                        contents['entries'][goal_to_be_completed - 1]['status'] = 1
                        input_data(contents, GOALS_CONFIG_FILE_PATH)
                        not_valid_goal_number = 0
    else:
        click.echo(chalk.red(
            'There are no goals set. Set a new goal by entering "yoda goals new"'))

def goal_name_exists(goal_name):
    file_name = get_goal_file_path(goal_name)
    return os.path.isfile(file_name)

def new_goal():
    """
    new goal
    """

    goals_dir_check()

    click.echo(chalk.blue('Input a single-word name of the goal:'))
    goal_name = input().strip()

    if goal_name_exists(goal_name):
        click.echo(chalk.red(
            'A goal with this name already exists. Please type "yoda goals view" to see a list of existing goals'))
    else:
        click.echo(chalk.blue('Input description of the goal:'))
        text = input().strip()

        click.echo(chalk.blue('Input due date for the goal (YYYY-MM-DD):'))
        deadline = input().strip()

        if os.path.isfile(GOALS_CONFIG_FILE_PATH):
            setup_data = dict(
                name=goal_name,
                text=text,
                deadline=deadline,
                status=0
            )
            append_data_into_file(setup_data, GOALS_CONFIG_FILE_PATH)
        else:
            setup_data = dict(
                entries=[
                    dict(
                        name=goal_name,
                        text=text,
                        deadline=deadline,
                        status=0
                    )
                ]
            )
            input_data(setup_data, GOALS_CONFIG_FILE_PATH)

        input_data(dict(entries=[]), get_goal_file_path(goal_name))

def goals_analysis():
    """
    goals alysis
    """

    now = datetime.datetime.now()

    total_goals = 0
    total_incomplete_goals = 0
    total_missed_goals = 0
    total_goals_next_week = 0
    total_goals_next_month = 0

    if os.path.isfile(GOALS_CONFIG_FILE_PATH):
        with open(GOALS_CONFIG_FILE_PATH) as goals_file:
            contents = yaml.load(goals_file)
            for entry in contents['entries']:
                total_goals += 1
                if entry['status'] == 0:
                    total_incomplete_goals += 1
                    deadline = datetime.datetime.strptime(entry['deadline'], '%Y-%m-%d')
                    total_missed_goals += (1 if deadline < now else 0)
                    total_goals_next_week += (1 if (deadline-now).days <= 7 else 0)
                    total_goals_next_month += (1 if (deadline - now).days <= 30 else 0)
        percent_incomplete_goals = total_incomplete_goals * 100 / total_goals
        percent_complete_goals = 100 - percent_incomplete_goals

        click.echo(chalk.red('Percentage of incomplete goals : ' + str(percent_incomplete_goals)))
        click.echo(chalk.green('Percentage of completed goals : ' + str(percent_complete_goals)))
        click.echo(chalk.blue('Number of missed deadlines : ' + str(total_missed_goals)))
        click.echo(chalk.blue('Number of goals due within the next week : ' + str(total_goals_next_week)))
        click.echo(chalk.blue('Number of goals due within the next month : ' + str(total_goals_next_month)))

    else:
        click.echo(chalk.red(
            'There are no goals set. Set a new goal by entering "yoda goals new"'))


def add_task_to_goal(goal_name, date, timestamp):
    goal_filename = get_goal_file_path(goal_name)
    if os.path.isfile(goal_filename):
        setup_data = dict(
            date=date,
            timestamp=timestamp
        )
        append_data_into_file(setup_data, goal_filename)
        return True
    return False

def list_goals():
    """
    get goals listed chronologically by deadlines
    """
    if os.path.isfile(GOALS_CONFIG_FILE_PATH):

        with open(GOALS_CONFIG_FILE_PATH) as goals_file:
            contents = yaml.load(goals_file)

            if len(contents):
                contents['entries'].sort(key=lambda x: x['deadline'].split('-'))

                click.echo('Goals')
                click.echo('----------------')
                click.echo("Status |  Deadline   | Name: text")
                click.echo("-------|-------------|---------------")
                incomplete_goals = 0
                total_tasks = 0
                total_missed_deadline = 0

                for entry in contents['entries']:
                    total_tasks += 1
                    incomplete_goals += (1 if entry['status'] == 0 else 0)
                    deadline = entry['deadline']
                    name = entry['name']
                    text = entry['text'] if entry['status'] == 0 else strike(
                        entry['text'])
                    status = "O" if entry['status'] == 0 else "X"

                    deadline_time = datetime.datetime.strptime(deadline, '%Y-%m-%d')
                    now = datetime.datetime.now()

                    total_missed_deadline += (1 if deadline_time < now else 0)

                    click.echo("   " + status + "   | " + deadline + "  | #" + name + ": " + text)

                click.echo('----------------')
                click.echo('')
                click.echo('Summary:')
                click.echo('----------------')

                if incomplete_goals == 0:
                    click.echo(chalk.green(
                        'All goals have been completed! Set a new goal by entering "yoda goals new"'))
                else:
                    click.echo(chalk.red("Incomplete tasks: " + str(incomplete_goals)))
                    click.echo(chalk.red("Tasks with missed deadline: " + str(total_missed_deadline)))
                    click.echo(chalk.green("Completed tasks: " +
                                           str(total_tasks - incomplete_goals)))

            else:
                click.echo(
                    'There are no goals set. Set a new goal by entering "yoda goals new"')

    else:
        click.echo(
            'There are no goals set. Set a new goal by entering "yoda goals new"')


def view_related_tasks():
    """
    list tasks assigned to the goal
    """

    from .diary import get_task_info

    not_valid_name = True

    if os.path.isfile(GOALS_CONFIG_FILE_PATH):
        while not_valid_name:
            click.echo(chalk.blue(
                'Enter the goal name that you would like to examine'))
            goal_name = input()
            goal_file_name = get_goal_file_path(goal_name)
            if os.path.isfile(goal_file_name):
                not_valid_name = False

        with open(goal_file_name) as goals_file:
            contents = yaml.load(goals_file)

            if len(contents['entries']):

                total_tasks = 0
                total_incomplete = 0

                click.echo('Tasks assigned to the goal:')
                click.echo('----------------')
                click.echo("Status |  Date   | Text")
                click.echo("-------|---------|-----")

                for entry in contents['entries']:
                    timestamp = entry['timestamp']
                    date = entry['date']
                    status, text = get_task_info(timestamp, date)
                    total_tasks += 1
                    total_incomplete += (1 if status == 0 else 0)

                    text = text if status == 0 else strike(text)
                    status = "O" if status == 0 else "X"
                    click.echo("   " + status + "   | " + date + "| " + text)

                click.echo('----------------')
                click.echo('')
                click.echo('Summary:')
                click.echo('----------------')

                click.echo(chalk.red("Incomplete tasks assigned to the goal: " + str(total_incomplete)))
                click.echo(chalk.green("Completed tasks assigned to the goal: " +
                                       str(total_tasks - total_incomplete)))

            else:
                click.echo(chalk.red(
                    'There are no tasks assigned to the goal. Add a new task by entering "yoda diary nt"'))

    else:
        click.echo(chalk.red(
            'There are no goals set. Set a new goal by entering "yoda goals new"'))

