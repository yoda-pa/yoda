import os
import sys
import json

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
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
def chat(ctx, input):
    """
    A simple chatbot\n
    To use, type: yoda chat <message>
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.chat"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


# The devtools module
cli.add_command(dev.dev)
cli.add_command(dev.speedtest)
cli.add_command(dev.url)
cli.add_command(dev.hackernews)
cli.add_command(dev.coinflip)
cli.add_command(dev.iplookup)
cli.add_command(dev.ciphers)
cli.add_command(dev.checksite)
cli.add_command(dev.horoscope)
cli.add_command(dev.gitsummary)
cli.add_command(dev.mp3cutter)
cli.add_command(dev.whois)
cli.add_command(dev.fileshare)
cli.add_command(dev.run)
cli.add_command(dev.keybindings)

# custom commands
cli.add_command(dev.cc)


def _rename(newname):
    def decorator(f):
        f.__name__ = newname
        f.__doc__ = 'Custom command: "{0}"'.format(newname)
        return f
    return decorator


def _create_custom_command(command):
    @cli.command()
    @_rename(str(command))
    def f():
        os.system(command)

    return f;


if os.path.isdir('resources/custom_commands'):
    with open('resources/custom_commands/custom_commands.json') as f:
        data = json.load(f)

        for command in data:
            cli.add_command(_create_custom_command(command))

@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
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
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.love"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
def people(ctx, input):
    """
    maintain a profile of someone your Friend\n

    commands:\n
    setup: Setup Friend\n
    status: check Friend status\n
    note: Add a note\n
    notes: View notes\n
    like: Add things they like\n
    likes: View things they like\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.people"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
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
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.diary"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
def money(ctx, input):
    """
    For tracking money \n\n
    Commands:\n
    setup: set a profile with default currency and initial money\n
    status: check config\n
    exp: add an expense\n
    exps: view all expenses\n
    convert: Convert from one currency to other\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.money"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


# The food module
cli.add_command(food.food)
# The learn module
cli.add_command(learn.learn)
cli.add_command(learn.vocabulary)
cli.add_command(learn.flashcards)
cli.add_command(learn.dictionary)

# The entertainment module
cli.add_command(entertainment.lyrics)


@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
def setup(ctx, input):
    """
    create a setup configuration for you to save some information locally

    Commands:\n
    new: Create a setup configuration\n
    check: Check existing setup\n
    delete: Delete existing setup\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.setup"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


# feedback
@cli.command()
def feedback():
    """
    Provide feedback for this package by:\n
    - Reporting a bug
    - Suggesting a feature
    - General suggestion
    """
    click.echo(
        "For:\n\
    1. reporting a bug\n\
    2. For suggesting a feature\n\
    3. Any general suggestion or question\n\
Please create an issue in the Github repository:\nhttps://github.com/yoda-pa/yoda/issues/new"
    )


# the life module
cli.add_command(life.rlist)
cli.add_command(life.ideas)
cli.add_command(life.leaselist)


@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
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
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.goals"].process(test_string)
    else:
        click.echo("No input specified. Run with --help for info")


@cli.command()
@click.pass_context
@click.argument("input", nargs=1, required=True, callback=alias.alias_checker)
def ascii_transform(ctx, input):
    """
    Transform an image into ascii \n\n
    Pass the absolute path to  the image as the argument\n
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ""
        for i in input:
            test_string += i + ""
        data = sys.modules["modules.asciiator"].process(str(test_string))
    else:
        click.echo("No input specified. Run with --help for info")
    print(data)

cli.add_command(gif.gif)

from modules import weather


@cli.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias.alias_checker)
def weather(ctx, input):
    """
    Get weather\n
    To use, type: yoda weather <location>
    """
    input = util.get_arguments(ctx, -1)
    if input:
        test_string = ""
        for i in input:
            test_string += i + " "
        data = sys.modules["modules.weather"].get_weather(test_string)
    else:
        click.echo('No input specified. Run with --help for info')
        
from modules import keep
cli.add_command(keep.keep)
