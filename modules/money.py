import click
import chalk

def process(input):
    click.echo(chalk.green('you are in money module'))
    click.echo('input = %s' % input)
