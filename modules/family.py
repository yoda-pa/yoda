import click
import chalk

def process(input):
    click.echo(chalk.blue('you are in family module'))
    click.echo('input = %s' % input)
