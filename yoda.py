import os
import sys

import click

from modules import *

sys.path.insert(1, os.getcwd())

@click.group(cls=alias.Alias)
@click.pass_context
def cli(ctx):
    """
    Yoda PA: A personal assistant based on the command line
    """

# The alias module
cli.add_command(alias.alias)


@cli.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias.alias_checker)
def chat(ctx, input):
    """
    A simple chatbot\n
    To use, type: yoda chat <message>
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ''
        for i in input:
            test_string += i + ' '
        data = sys.modules['modules.chat'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


# The devtools module
cli.add_command(dev.dev)
cli.add_command(dev.speedtest)
cli.add_command(dev.url)
cli.add_command(dev.hackernews)
cli.add_command(dev.coinflip)


@cli.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias.alias_checker)
def love(ctx, input):
    """
    maintain a profile of someone you love\n

    commands:\n
    setup: Setup love\n
    status: check love status\n
    note: Add a note\n
    notes: View notes\n
    like: Add things they like\n
    likes: View things they like\n
    addbirth: Add birthday\n
    showbirth: Show birthday\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.love'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


@cli.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias.alias_checker)
def diary(ctx, input):
    """
    Maintain a personal diary\n
    roughly based on the concept of Bullet Journal (http://bulletjournal.com/) \n\n

    Commands:\n
    nn: New note\n
    nt: new Task\n
    dt: delete task\n
    notes: view all notes\n
    ut: update task\n
    un: update note\n
    dct: delete all completed tasks\n
    dn:delete particular note\n
    tasks: view all completed and incomplete tasks\n
    ct: complete task
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.diary'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')


@cli.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias.alias_checker)
def money(ctx, input):
    """
    For tracking money \n\n
    Commands:\n
    setup: set a profile with default currency and initial money\n
    status: check config\n
    exp: add an expense\n
    exps: view all expenses\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.money'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')

# The food module
cli.add_command(food.food)
# The learn module
cli.add_command(learn.learn)
cli.add_command(learn.vocabulary)
cli.add_command(learn.flashcards)
cli.add_command(learn.define)


@cli.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias.alias_checker)
def setup(ctx, input):
    """
    create a setup configuration for you to save some information locally
    """
    input = util.get_arguments(ctx, -1)
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

@cli.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias.alias_checker)
def goals(ctx, input):
    """
    Set your goals \n\n

    Commands:\n
    new: New goal\n
    view: View all completed and incomplete goals\n
    tasks: View tasks related to the goal\n
    complete: Complete a goal\n
    analyze: Analyze goals\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        data = sys.modules['modules.goals'].process(test_string)
    else:
        click.echo('No input specified. Run with --help for info')
