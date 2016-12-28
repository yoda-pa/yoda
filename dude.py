import click

@click.command()
@click.argument('input', nargs=-1)
def cli(input):
	''' This is the greeting string '''
	click.echo(input)
