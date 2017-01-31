import click
import chalk

def process(input):
    click.echo(chalk.blue('you are in fashion module'))
    click.echo('input = %s' % input)
