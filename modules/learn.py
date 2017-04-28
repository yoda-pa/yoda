import click
import chalk

def new():
    print("Enter something you want to learn")

# command checker
def check_sub_command(c):
    sub_commands = {
        'new' : new
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude learn --help" for more info')

# the main process
def process(input):
    input = input.lower().strip()
    check_sub_command(input)
