import click
import chalk
import sys
import os
sys.path.insert(1, os.getcwd())
from modules import *


@click.group()
def cli():
    ''' Yoda PA: A personal assistant based on the command line '''

# git


@cli.command()
@click.argument('input', nargs=-1)
def git(input):
    '''
    Helps with your git operations\n
    ------------------------------\n
    Some commands that can be used:\n
    yoda git all status  - goes into all repos in current directory and shows the status of all\n
    yoda git credentials - shows your credentials. If not set, it would prompt for input\n
    yoda git agenda      - Show all the repos worked on in the past and suggest which ones should be worked on depending on commits etc\n
    yoda git push all    - Pushes everything with automatically generated commits (you will have the option to manually enter the commit messages before committing)\n
    '''
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.git'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# chat


@cli.command()
@click.argument('input', nargs=-1)
def chat(input):
    '''
    A simple chatbot\n
    To use, type: yoda chat <message>
    '''
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

# family


@cli.command()
@click.argument('input', nargs=-1)
def family(input):
    ''' family '''
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.family'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# love


@cli.command()
@click.argument('input', nargs=-1)
def love(input):
    ''' maintain a profile of someone you love '''
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.love'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# diary


@cli.command()
@click.argument('input', nargs=-1)
def diary(input):
    ''' Maintain a personal diary\n
    roughly based on the concept of Bullet Journal (http://bulletjournal.com/) \n\n

    Commands:\n
    nn: New note\n
    nt: new Task\n
    notes: view all notes\n
    tasks: view all completed and incomplete tasks\n
    ct: complete task
    '''
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.diary'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# money


@cli.command()
@click.argument('input', nargs=-1)
def money(input):
    ''' For tracking money \n\n
    Commands:\n
    setup: set a profile with default currency and initial money\n
    status: check config\n
    exp: add an expense\n
    exps: view all expenses\n
    '''
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

# health


@cli.command()
@click.argument('input', nargs=-1)
def health(input):
    ''' health '''
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.health'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# fashion


@cli.command()
@click.argument('input', nargs=-1)
def fashion(input):
    ''' fashion '''
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.fashion'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# setup


@cli.command()
@click.argument('input', nargs=-1)
def setup(input):
    ''' create a setup configuration for you to save some information locally '''
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
    '''
    Provide feedback for this package by:\n
    - Reporting a bug
    - Suggesting a feature
    - General suggestion
    '''
    click.echo('For:\n\
    1. reporting a bug\n\
    2. For suggesting a feature\n\
    3. Any general suggestion or question\n\
Please create an issue in the Github repository:\nhttps://github.com/yoda-pa/yoda/issues/new')


# life.reading_list module
cli.add_command(life.rlist)

#life.idea_list module
cli.add_command(life.ideas)
