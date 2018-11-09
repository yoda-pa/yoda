from __future__ import division
from __future__ import absolute_import
from builtins import input
from builtins import str
from past.utils import old_div
import json
import os.path
import time

from Crypto.Cipher import AES

from .config import get_config_file_paths
from modules.setup import cypher_pass_generator
from .util import *
from .alias import alias_checker

# config file path
LIFE_CONFIG_FILE_PATH = get_config_file_paths()["LIFE_CONFIG_FILE_PATH"]
LIFE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(LIFE_CONFIG_FILE_PATH)
RLIST_PARAMS = ("title", "author", "kind", "tags")


def is_in_params(params, query, article):
    """
    Get file path for today's tasks entry file

    :param params:
    :param query:
    :param article:
    :return:
    """
    query = query.lower()
    article_filter = article[params]

    if type(article_filter) is list:
        article_filter = [item.lower() for item in article_filter]
    else:
        article_filter = article_filter.lower()

    return query in article_filter


@click.group()
def life():
    """
        Life command group:\n
        contains helpful commands to organize your life
    """


def reading_list_entry_file_path():
    """
    Get complete path of the file reading_list.yaml
    :return: path
    """
    return os.path.join(LIFE_CONFIG_FOLDER_PATH, "reading_list.yaml")


READING_LIST_ENTRY_FILE_PATH = reading_list_entry_file_path()


def empty_list_prompt():
    """
    Empty list prompt
    """
    click.echo(
        "You reading list is empty. Add something to the list, do you want to? (Y/n)"
    )
    decision = get_input().lower()

    if decision == "y" or not decision:
        add_to_reading_list()
    else:
        click.echo("Using 'yoda rlist add', you can create later.")


def print_reading_list(reading_list_contents, only=RLIST_PARAMS):
    """
    prints reading list
    :param reading_list_contents:
    :param only:
    """
    for i, entry in enumerate(reading_list_contents["entries"]):
        click.echo("-" + ("[" + str(i) + "]").ljust(24, "-"))
        title = entry["title"]
        author = entry["author"]
        kind = entry["kind"]
        tags = entry["tags"]

        click.echo("Title: " + title) if title and "title" in only else None
        click.echo("Author: " + author) if author and "author" in only else None
        click.echo("Kind: " + kind) if kind and "kind" in only else None
        click.echo("Tags: " + ", ".join(tags)) if tags and "tags" in only else None

    click.echo("---END-OF-READING-LIST---")


def view_reading_list(opts):
    """
    get the current reading list
    :param opts:
    """
    if os.path.isfile(READING_LIST_ENTRY_FILE_PATH):
        with open(READING_LIST_ENTRY_FILE_PATH) as reading_list_entry:
            file_contents = yaml.load(reading_list_entry)
            file_contents = dict(file_contents)
            last_updated = time.ctime(os.path.getmtime(READING_LIST_ENTRY_FILE_PATH))
            query = opts[1]
            params = opts[0]
            search = ""

            if query != "None":
                search = "(filtered by " + params + ": " + query + ")"
                filtered_contents = [
                    article
                    for article in file_contents["entries"]
                    if is_in_params(params, query, article)
                ]
                file_contents = dict(entries=filtered_contents)

            click.echo(chalk.blue("Your awesome reading list " + search))
            click.echo(chalk.blue("Last updated: " + last_updated))
            print_reading_list(file_contents)
    else:
        empty_list_prompt()


def add_to_reading_list(query=""):
    """
    add anything to the reading list
    :param query:
    """
    click.echo(chalk.blue("Title of the article:"))
    _title = get_input()
    while len(_title) == 0:
        click.echo(chalk.red("No title, cannot be."))
        click.echo(chalk.blue("Title of the article:"))
        _title = get_input()

    click.echo(chalk.blue("Author of the article:"))
    _author = get_input()

    click.echo(
        chalk.blue("Article type/kind/genre (e.g. book, article, blog, sci-fi):")
    )
    _kind = get_input()

    click.echo(chalk.blue("Tags for easier filtering/searching (seperated by spaces):"))
    _tags = get_input().split()

    setup_data = dict(title=_title, author=_author, kind=_kind, tags=_tags)

    if os.path.isfile(READING_LIST_ENTRY_FILE_PATH):
        append_data_into_file(setup_data, READING_LIST_ENTRY_FILE_PATH)
    else:
        setup_data = dict(entries=[setup_data])
        create_folder(os.path.join(LIFE_CONFIG_FOLDER_PATH, "rlist"))
        input_data(setup_data, READING_LIST_ENTRY_FILE_PATH)

    click.echo(chalk.blue("Added " + _title + " to your reading list!"))


# the rlist process


@life.command()
@click.argument("subcommand", nargs=1)
@click.option("--params", nargs=1, required=False, default="tags")
@click.argument("query", nargs=1, required=False)
def rlist(sub_command, params, query):
    """
        Reading list for your daily life

        yoda rlist [OPTIONS] SUBCOMMAND [QUERY]

        ACTION:

            view [--params="tags"] [query]: view your reading list

                params: reading list parameter to be filtered (defaults to tags)

                query: keyword to be searched

            add: add something to your reading list
    """
    sub_command = str(sub_command)
    params = str(params)
    query = str(query)
    opts = (params, query) if params and query else ()
    # print opts
    sub_commands = {"view": view_reading_list, "add": add_to_reading_list}
    try:
        sub_commands[sub_command](opts)
    except KeyError:
        click.echo(chalk.red("Command " + sub_command + " does not exist!"))
        click.echo("Try 'yoda rlist --help' for more info'")


# idea list operations

# config file path

IDEA_CONFIG_FILE_PATH = get_config_file_paths()["IDEA_CONFIG_FILE_PATH"]
CONFIG_FILE_PATH = get_config_file_paths()["USER_CONFIG_FILE_PATH"]
cipher_key = cypher_pass_generator()
cipher_IV456 = cypher_pass_generator()

setup_data = dict(
    name="",
    email="",
    github=dict(username="", password=""),
    encryption=dict(cipher_key=cipher_key, cipher_IV456=cipher_IV456),
)

if not os.path.exists(os.path.dirname(CONFIG_FILE_PATH)):
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE_PATH))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

if not os.path.isfile(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        yaml.dump(setup_data, config_file, default_flow_style=False)

config_file = open(CONFIG_FILE_PATH)
contents = yaml.load(config_file)
cipher_key = contents["encryption"]["cipher_key"]
cipher_IV456 = contents["encryption"]["cipher_IV456"]


def encryption(text):
    """
    encryption function for saving ideas
    :param text:
    :return:
    """
    return AES.new(cipher_key, AES.MODE_CBC, cipher_IV456).encrypt(text * 16)


def decryption(text):
    """
    decryption function for saving ideas
    :param text:
    :return:
    """
    s = AES.new(cipher_key, AES.MODE_CBC, cipher_IV456).decrypt(text)
    return s[: old_div(len(s), 16)]


def add_idea(project_name, task_name):
    """
    a new entry created
    :param project_name:
    :param task_name:
    """
    try:
        with open(IDEA_CONFIG_FILE_PATH) as f:
            data = f.read()
            data = decryption(data)
            data = json.loads(data)
        f.close()
    except:
        data = None
    if not isinstance(data, dict):
        data = dict()
    if project_name in data:
        task = data[project_name]
    else:
        task = []

    click.echo(chalk.blue("Brief desc of the current task : "))
    desc = input()
    task.append((task_name, desc))  # a new entry created
    data[project_name] = task
    with open(IDEA_CONFIG_FILE_PATH, "w") as f:
        data = json.dumps(data)
        data = encryption(data)
        f.write(data)
    f.close()


def show(project_name, task_name):
    """
    all the saved entries are displayed
    :param project_name:
    :param task_name:
    :return:
    """
    try:
        with open(IDEA_CONFIG_FILE_PATH) as f:
            data = f.read()
            data = decryption(data)
            data = json.loads(data)
        f.close()
    except:
        click.echo(
            chalk.red(
                'There are no saved ideas for now. Please run "yoda ideas add" to add a new idea'
            )
        )
        return
    for proj, task in list(data.items()):
        click.echo(chalk.yellow(proj))
        for _task_name, _task_description in task:
            click.echo(chalk.cyan("\t" + _task_name))
            click.echo(chalk.cyan("\t\t" + _task_description))


def remove(project, task=None):
    """
    delete a whole entry or a sub-entry inside it
    :param project:
    :param task:
    :return:
    """
    try:
        with open(IDEA_CONFIG_FILE_PATH) as f:
            data = f.read()
            data = decryption(data)
            data = json.loads(data)
        f.close()
    except:
        click.echo(chalk.red("File not exist, operation aborted."))
        return
    f.close()
    try:
        if task is None:
            del data[project]  # a project deleted
            click.echo(chalk.blue("Project deleted successfully."))
        else:
            data[project] = [
                x for x in data[project] if x[0] != task
            ]  # task inside a respective project deleted
            click.echo(chalk.blue("Task deleted successfully."))
        with open(IDEA_CONFIG_FILE_PATH, "w") as f:
            data = json.dumps(data)
            data = encryption(data)
            f.write(data)
        f.close()
    except:
        click.echo(
            chalk.red(
                "Wrong task or project entered. Please check using 'yoda ideas show'"
            )
        )


# idea list process
@life.command()
@click.argument("subcommand", nargs=1)
@click.option("--task", nargs=1, required=False, default=None)
@click.option("--project", nargs=1, required=False, default=None)
@click.option("--inside", nargs=1, required=False, default=None)
def ideas(subcommand, task, project, inside):
    """
        Keep track of your precious ideas.

        yoda ideas SUBCOMMAND [OPTIONAL ARGUMENTS]

        ACTION:

            show   : list out all the exiting ideas

            add    : add a project or a task inside a project. You need to use either --project or --inside flag to
            add a new project/task

            remove : delete a task or a complete project. You need to use either --project or --inside flag to
            remove a project/task

    """
    if subcommand != "show" and (project or inside) is None:
        click.echo(
            chalk.red(
                "Operation aborted. You have not selected any project or task. Please use this command with either "
                "--project or --inside flag"
            )
        )
        return
    sub_commands = {"show": show, "add": add_idea, "remove": remove}
    try:
        sub_commands[subcommand]((project or inside), task)
    except KeyError:
        click.echo(chalk.red("Command " + subcommand + " does not exist."))
        click.echo('Try "yoda ideas --help" for more info')
