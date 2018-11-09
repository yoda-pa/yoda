from __future__ import absolute_import
from builtins import str
from builtins import input
import datetime
from .config import get_config_file_paths
from .util import *

# config file path
PEOPLE_CONFIG_FILE_PATH = get_config_file_paths()["PEOPLE_CONFIG_FILE_PATH"]
PEOPLE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(PEOPLE_CONFIG_FILE_PATH)


def get_friends_file_path(friend_name):
    """
    get file path for friend's entry file
    :return:
    """
    return PEOPLE_CONFIG_FOLDER_PATH + "/" + friend_name + ".yaml"


def friend_name_exists(friend_name):
    file_name = get_friends_file_path(friend_name)
    return os.path.isfile(file_name)


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


def status():
    """
    check status
    """
    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        with open(PEOPLE_CONFIG_FILE_PATH) as config_file:
            contents = yaml.load(config_file)
            entries = contents["entries"]
            click.echo("People:")
            click.echo("--------------------------------------")
            click.echo("     Mob    |     DOB    |   Name     ")
            click.echo("------------|------------|------------")
            for i, entry in enumerate(entries):
                s_no = str(i)
                name = entry["name"]
                dob = entry["dob"]
                mob = entry["mobile"]
                click.echo(" " + mob + " | " + dob + " | " + name)
    else:
        click.echo(
            chalk.red(
                'The configuration file for this module does not exist. Please type "yoda people setup" to create a new one'
            )
        )


def setup():
    """
    create new setup
    :return:
    """
    create_folder(PEOPLE_CONFIG_FOLDER_PATH)

    click.echo(chalk.blue("Enter their name:"))
    name = input().strip().lower()

    if friend_name_exists(name):
        click.echo(
            chalk.red(
                'A configuration with this friend name already exists.Please type "yoda people --help"'
            )
        )

    click.echo(chalk.blue("Input their DOB (YYYY-MM-DD):"))
    incorrect_date_format = True
    while incorrect_date_format:
        dob = input().strip()
        try:
            date_str = datetime.datetime.strptime(dob, "%Y-%m-%d").strftime("%Y-%m-%d")
            if date_str != dob:
                raise ValueError
            incorrect_date_format = False
        except ValueError:
            click.echo(
                chalk.red("Incorrect data format, should be YYYY-MM-DD. Please repeat:")
            )

    click.echo(chalk.blue("Enter their Mobile Number:"))
    mobile = input().strip()

    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        setup_data = dict(name=name, mobile=mobile, dob=dob)
        append_data_into_file(setup_data, PEOPLE_CONFIG_FILE_PATH)
    else:
        setup_data = dict(entries=[dict(name=name, mobile=mobile, dob=dob)])
        input_data(setup_data, PEOPLE_CONFIG_FILE_PATH)

    input_data(dict(entries=[]), get_friends_file_path(name))


def like():
    """
    Adds likes
    """
    click.echo(chalk.blue("For whom you want to add like for"))
    friend_name = input().strip().lower()

    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        hashtags = []
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
        if "likes" in entries:
            notes = entries["likes"]
            del entries["likes"]
        continue_adding_hashtags = True
        while continue_adding_hashtags:
            click.echo(chalk.blue("Enter what they like or -"))
            hashtag = input().strip()
            if hashtag == "-":
                continue_adding_hashtags = False
            else:
                hashtags.append("#" + hashtag)

        setup_data = dict(likes=hashtags)
        append_data_into_file(setup_data, FRIENDS_FILE_PATH)
    else:
        click.echo(
            chalk.red(
                "Friend's config file doesn't exist. Type 'yoda people setup' to setup a friend"
            )
        )


def note():
    """
    Adds notes
    """
    click.echo(chalk.blue("For whom you want to add a note for"))
    friend_name = input().strip().lower()

    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        notes = []
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
        if "notes" in entries:
            notes = entries["notes"]
            del entries["notes"]
        continue_adding_notes = True
        while continue_adding_notes:
            click.echo(chalk.blue("Enter note or press -"))
            note = input().strip()
            if note == "-":
                continue_adding_notes = False
            else:
                notes.append(note)

        setup_data = dict(notes=notes)
        append_data_into_file(setup_data, FRIENDS_FILE_PATH)
    else:
        click.echo(
            chalk.red(
                "Friend's config file doesn't exist. Type 'yoda people setup' to setup a friend"
            )
        )


def likes():
    """
    view the things they like
    """
    click.echo(chalk.blue("For whom you want to view likes for"))
    friend_name = input().strip().lower()
    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
            likes = []
            for entry in entries:
                if "likes" in entry:
                    likes.extend(entry["likes"])
            click.echo("Likes:")
            for i, n in enumerate(likes):
                click.echo(str(i) + ": " + n)
    else:
        click.echo(
            chalk.red(
                'The Likes file path for this module does not exist. Please type "yoda people like" to create a new one'
            )
        )


def notes():
    """
    view notes
    """
    click.echo(chalk.blue("For whom you want to view notes for"))
    friend_name = input().strip().lower()
    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
            notes = []
            for entry in entries:
                if "notes" in entry:
                    notes.extend(entry["notes"])
            click.echo("Notes:")
            for i, n in enumerate(notes):
                click.echo(str(i) + ": " + n)
    else:
        click.echo(
            chalk.red(
                'The Notes file path for this module does not exist. Please type "yoda people note" to create a new one'
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
        # 'addbirth': addbirth,
        # 'showbirth': showbirth
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
