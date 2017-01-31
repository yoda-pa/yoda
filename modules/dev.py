import click
import chalk

def process(input):
    click.echo(chalk.blue('you are in dev module'))
    click.echo('input = %s' % input)
