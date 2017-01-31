import click
import chalk

def process(input):
    click.echo(chalk.blue('you are in diary module'))
    click.echo('input = %s' % input)
