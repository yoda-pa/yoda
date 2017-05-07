import click
import chalk


def process(input):
    click.echo(chalk.blue('you are in health module'))
    click.echo('input = %s' % input)
