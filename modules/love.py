import click
import chalk

def process(input):
    click.echo(chalk.red('you are in love module'))
    click.echo('input = %s' % input)
