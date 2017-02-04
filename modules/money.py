import click
import chalk
import platform

def status():
    click.echo('status will be displayed')

def setup():
    click.echo('setup will be done')

def check_sub_command(c):
    options = {
        'status' : status,
        'setup' : setup
    }
    return options[c]()

# the main process
def process(input):
    click.echo(chalk.green('you are in money module'))
    input = input.lower().strip()
    click.echo('input = %s' % input)
    check_sub_command(input)
    click.echo(platform.system())
