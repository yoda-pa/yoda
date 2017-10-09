import click
from config import get_config_file_paths
import os.path
import time
from util import *


# config file path
LIFE_CONFIG_FILE_PATH = get_config_file_paths()['LIFE_CONFIG_FILE_PATH']
LIFE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    LIFE_CONFIG_FILE_PATH)
RLIST_PARAMS = ('title', 'author', 'kind', 'tags')

# get file path for today's tasks entry file

def is_in_params(params, query, article):
    query = query.lower()
    filter = article[params]

    if type(filter) is list:
        filter = [ item.lower() for item in filter ]
    else:
        filter = filter.lower()

    return (query in filter)

@click.group()
def life():
    '''
        Life command group:\n
        contains helpful commands to organize your life
    '''


def reading_list_entry_file_path():
    return os.path.join(LIFE_CONFIG_FOLDER_PATH, "reading_list.yaml")


READING_LIST_ENTRY_FILE_PATH = reading_list_entry_file_path()

# asks user to create a reading list if s/he has none


def empty_list_prompt():
    click.echo("You reading list is empty. Add something to the list, you want to? (Y/n)")
    decision = get_input().lower()

    if decision == "y" or not decision:
        add_to_rlist()
    else:
        click.echo("Using 'yoda rlist add', you can create later.")

# prints reading list


def print_rlist(contents, only=RLIST_PARAMS):
    i = 0
    for entry in contents['entries']:
        i+=1
        click.echo("-" + ('['+str(i)+']').ljust(24, '-'))
        title = entry['title']
        author = entry['author']
        kind = entry['kind']
        tags = entry['tags']

        click.echo("Title: " + title) if title and 'title' in only else None
        click.echo("Author: " + author) if author and 'author' in only else None
        click.echo("Kind: " + kind) if kind and 'kind' in only else None
        click.echo("Tags: " + ", ".join(tags)) if tags and 'tags' in only else None

    click.echo("---END-OF-READING-LIST---")

# get the current reading list


def view_rlist(opts):
    if os.path.isfile(READING_LIST_ENTRY_FILE_PATH):
        with open(READING_LIST_ENTRY_FILE_PATH, 'r') as reading_list_entry:
            contents = yaml.load(reading_list_entry)
            contents = dict(contents)
            last_updated = time.ctime(os.path.getmtime(READING_LIST_ENTRY_FILE_PATH))
            query = opts[1]
            params = opts[0]
            search = ''

            if query != 'None':
                search = "(filtered by " + params + ": " + query + ")"
                filtered_contents = [ article for article in contents['entries'] if is_in_params(params, query, article) ]
                contents = dict(entries=filtered_contents)


            chalk.blue("Your awesome reading list " + search)
            chalk.blue("Last updated: " + last_updated)
            print_rlist(contents)
    else:
        empty_list_prompt()

# add anything to the reading list


def add_to_rlist(query=""):
    chalk.blue("Title of the article:")
    _title = get_input()
    while len(_title) == 0:
        chalk.red("No title, cannot be.")
        chalk.blue("Title of the article:")
        _title = get_input()

    chalk.blue("Author of the article:")
    _author = get_input()

    chalk.blue("Article type/kind/genre (e.g. book, article, blog, sci-fi):")
    _kind = get_input()

    chalk.blue("Tags for easier filtering/searching (seperated by spaces):")
    _tags = get_input().split()

    setup_data = dict(
        title=_title,
        author=_author,
        kind=_kind,
        tags=_tags
    )

    if os.path.isfile(READING_LIST_ENTRY_FILE_PATH):
        append_data_into_file(setup_data, READING_LIST_ENTRY_FILE_PATH)
    else:
        setup_data = dict(entries=[setup_data])
        create_folder(os.path.join(LIFE_CONFIG_FOLDER_PATH, 'rlist'))
        input_data(setup_data, READING_LIST_ENTRY_FILE_PATH)

    chalk.blue("Added " + _title + " to your reading list!")

# the rlist process


@life.command()
@click.argument('subcommand', nargs=1)
@click.option('--params', nargs=1, required=False, default="tags")
@click.argument('query', nargs=1, required=False)
def rlist(subcommand, params, query):
    '''
        Reading list for your daily life

        yoda rlist [OPTIONS] SUBCOMMAND [QUERY]

        ACTION:

            view [--params="tags"] [query]: view your reading list

                params: reading list parameter to be filtered (defaults to tags)

                query: keyword to be searched

            add: add something to your reading list
    '''
    subcommand = str(subcommand)
    params = str(params)
    query = str(query)
    opts = (params, query) if params and query else ()
    subcommands = {
        'view': view_rlist,
        'add': add_to_rlist,
    }
    try:
        subcommands[subcommand](opts)
    except KeyError:
        chalk.red("Command " + subcommand + " does not exist!")
        click.echo("Try 'yoda rlist --help' for more info'")
