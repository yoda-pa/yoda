import os
import sys

import click

from modules import *

sys.path.insert(1, os.getcwd())


@click.group()
def cli():
    """
    Yoda PA: A personal assistant based on the command line
    """


@cli.command()
@click.argument('input', nargs=-1)
def chat(input):
    """
    A simple chatbot\n
    To use, type: yoda chat <message>
    """
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.chat'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


# The devtools module
cli.add_command(dev.dev)
cli.add_command(dev.speedtest)
cli.add_command(dev.url)
cli.add_command(dev.hackernews)


@cli.command()
@click.argument('input', nargs=-1)
def love(input):
    """
    maintain a profile of someone you love
    """
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.love'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


@cli.command()
@click.argument('input', nargs=-1)
def diary(input):
    """
    Maintain a personal diary\n
    roughly based on the concept of Bullet Journal (http://bulletjournal.com/) \n\n

    Commands:\n
    nn: New note\n
    nt: new Task\n
    notes: view all notes\n
    tasks: view all completed and incomplete tasks\n
    ct: complete task
    """
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.diary'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


@cli.command()
@click.argument('input', nargs=-1)
def money(input):
    """
    For tracking money \n\n
    Commands:\n
    setup: set a profile with default currency and initial money\n
    status: check config\n
    exp: add an expense\n
    exps: view all expenses\n
    """
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.money'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


# The learn module
cli.add_command(learn.learn)
cli.add_command(learn.vocabulary)
cli.add_command(learn.flashcards)
cli.add_command(learn.define)


@cli.command()
@click.argument('input', nargs=-1)
def setup(input):
    """
    create a setup configuration for you to save some information locally
    """
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.setup'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


# feedback
@cli.command()
def feedback():
    """
    Provide feedback for this package by:\n
    - Reporting a bug
    - Suggesting a feature
    - General suggestion
    """
    click.echo('For:\n\
    1. reporting a bug\n\
    2. For suggesting a feature\n\
    3. Any general suggestion or question\n\
Please create an issue in the Github repository:\nhttps://github.com/yoda-pa/yoda/issues/new')


# the life module
cli.add_command(life.rlist)
cli.add_command(life.ideas)
