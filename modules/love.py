from __future__ import absolute_import
from builtins import str
from builtins import input
from .config import get_config_file_paths
from .util import *

# config file path
LOVE_CONFIG_FILE_PATH = get_config_file_paths()["LOVE_CONFIG_FILE_PATH"]
LOVE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(LOVE_CONFIG_FILE_PATH)
LOVE_NOTES_FILE_PATH = LOVE_CONFIG_FOLDER_PATH + "/notes.yaml"
LOVE_LIKES_FILE_PATH = LOVE_CONFIG_FOLDER_PATH + "/likes.yaml"
LOVE_BIRTH_FILE_PATH = LOVE_CONFIG_FOLDER_PATH + "/birth.yaml"


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents["notes"].append(data)

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
        click.echo(
            chalk.red(
                'The configuration file for this module does not exist. Please type "yoda love setup" to create a new one'
            )
        )


def setup():
    """
    create new setup
    :return:
    """
    create_folder(LOVE_CONFIG_FOLDER_PATH)

    if ask_overwrite(LOVE_CONFIG_FILE_PATH):
        return

    click.echo(chalk.blue("Enter their name:"))
    name = input().strip()

    click.echo(chalk.blue("Enter sex(M/F):"))
    sex = input().strip()

    click.echo(chalk.blue("Where do they live?"))
    place = input().strip()

    setup_data = dict(name=name, place=place, sex=sex)

    input_data(setup_data, LOVE_CONFIG_FILE_PATH)


def note():
    """
    add a note for them
    """
    if os.path.isfile(LOVE_NOTES_FILE_PATH):
        data = dict(note=input())
        append_data_into_file(data, LOVE_NOTES_FILE_PATH)
    else:
        data = dict(notes=[dict(note=input())])
        input_data(data, LOVE_NOTES_FILE_PATH)


def notes():
    """
    view notes
    """
    if os.path.isfile(LOVE_NOTES_FILE_PATH):
        with open(LOVE_NOTES_FILE_PATH) as notes_file:
            contents = yaml.load(notes_file)
            click.echo("Notes:")
            for i, n in enumerate(contents["notes"]):
                click.echo(str(i) + ": " + n["note"])
    else:
        click.echo(
            chalk.red(
                'The notes file path for this module does not exist. Please type "yoda love note" to create a new one'
            )
        )


def append_like_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents["likes"].append(data)

        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)


def like():
    """
    add things they like
    """
    click.echo(chalk.blue("Add things they like"))
    if os.path.isfile(LOVE_LIKES_FILE_PATH):
        like_data = dict(like=input())
        append_like_data_into_file(like_data, LOVE_LIKES_FILE_PATH)
    else:
        like_data = dict(likes=[dict(like=input())])
        input_data(like_data, LOVE_LIKES_FILE_PATH)
    click.echo(chalk.blue("Want to add more things they like? [y/n]"))
    repeat = input()
    if repeat == "y" or repeat == "yes":
        like()


def likes():
    """
    view the things they like
    """
    if os.path.isfile(LOVE_LIKES_FILE_PATH):
        with open(LOVE_LIKES_FILE_PATH) as likes_file:
            contents = yaml.load(likes_file)
            click.echo("Likes:")
            for i, n in enumerate(contents["likes"]):
                click.echo(str(i) + ": " + n["like"])
    else:
        click.echo(
            chalk.red(
                'The Likes file path for this module does not exist. Please type "yoda love like" to create a new one'
            )
        )


def addbirth():
    """
    Add birthday 
    """
    if ask_overwrite(LOVE_BIRTH_FILE_PATH):
        return
    click.echo(chalk.blue("Enter birthday"))
    birthday = input()
    birth_data = dict(birthday=birthday)
    input_data(birth_data, LOVE_BIRTH_FILE_PATH)


def showbirth():
    """
    show birthday
    """
    if os.path.isfile(LOVE_BIRTH_FILE_PATH):
        with open(LOVE_BIRTH_FILE_PATH) as birth_file:
            contents = yaml.load(birth_file)
            click.echo("Birthday is " + contents["birthday"])
    else:
        click.echo(
            chalk.red(
                'The birth file for this module does not exist. Please type "yoda love addbirth" to create a new one'
            )
        )


def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        "setup": setup,
        "status": status,
        "note": note,
        "notes": notes,
        "likes": likes,
        "like": like,
        "addbirth": addbirth,
        "showbirth": showbirth,
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
        click.echo('Try "yoda love --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)
