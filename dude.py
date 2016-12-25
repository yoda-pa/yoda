import click

@click.command()
@click.option('--string', default='Dude', help='Sample string')
@click.option('--count', default=1, help='How many times to be repeated')
def cli(string, count):
	''' This is the greeting string '''
	for _ in xrange(count):
		click.echo('Hello, %s!' % string)
