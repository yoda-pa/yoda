import click
import chalk
from config import config_file_paths
import os.path
from os import listdir
import time
import yaml
from util import *


# config file path
LIFE_CONFIG_FILE_PATH = config_file_paths['LIFE_CONFIG_FILE_PATH']
LIFE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    LIFE_CONFIG_FILE_PATH)

# get file path for today's tasks entry file


def reading_list_entry_file_path():
    return LIFE_CONFIG_FOLDER_PATH + '/' + "reading_list.yaml"


READING_LIST_ENTRY_FILE_PATH = reading_list_entry_file_path()

# asks user to create a reading list if s/he has none


def empty_list_prompt():
    click.echo("You reading list is empty. Add something to the list, you want to? (Y/n)")
    decision = get_input().lower()

    if decision == "y" or not decision:
        add_to_rlist()
    else:
        click.echo("Using 'yoda life ra', you can create later.")

# prints reading list


def print_rlist(contents, only = ""):
    i = 0
    for entry in contents['entries']:
        i+=1
        click.echo("-" + ('['+str(i)+']').ljust(24, '-'))
        title = entry['title']
        author = entry['author']
        kind = entry['kind']
        tags = entry['tags']
        path = entry['path']

        click.echo("Title: " + title) if title or 'title' in only else ''
        click.echo("Author: " + author) if author or 'author' in only else ''
        click.echo("Kind: " + kind) if kind or 'kind' in only else ''
        click.echo("Tags: " + ", ".join(tags)) if tags or 'tags' in only else ''
        click.echo("Path: " + path) if path or 'path' in only else ''

    click.echo("---END-OF-READING-LIST---")

# get the current reading list


def rlist():
    if os.path.isfile(READING_LIST_ENTRY_FILE_PATH):
        with open(READING_LIST_ENTRY_FILE_PATH, 'r') as reading_list_entry:
            contents = yaml.load(reading_list_entry)
            last_updated = time.ctime(os.path.getmtime(READING_LIST_ENTRY_FILE_PATH))

            chalk.blue("Your awesome reading list")
            chalk.blue("Last updated: " + last_updated)

            contents = dict(contents)
            print_rlist(contents)
            # click.echo("Read something? Enter id")

            # key = int(get_input())
            # if key in range(1, len(contents['entries'])+1):
            #     article = contents['entries'][key-1]
            #     read_from_rlist(article)
            # else:
            #     click.echo("That is why you fail.")
    else:
        empty_list_promt()

# add anything to the reading list

def add_to_rlist():
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

    chalk.blue("Path to file, to start reading give me:")
    _path = get_input()

    setup_data = dict(
        title=_title,
        author=_author,
        kind=_kind,
        tags=_tags,
        path=_path
    )

    if os.path.isfile(READING_LIST_ENTRY_FILE_PATH):
        append_data_into_file(setup_data, READING_LIST_ENTRY_FILE_PATH)
    else:
        setup_data = dict(entries=[setup_data])
        input_data(setup_data, READING_LIST_ENTRY_FILE_PATH)

    chalk.blue("Added " + _title + " to your reading list!")

# command checker


def check_sub_command(c):
    sub_commands = {
        'rlist': rlist,
        'ra': add_to_rlist,
    }

    return sub_commands[c]()

# the main process


def process(input):
    input = input.lower().strip()
    check_sub_command(input)

