import click

@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
	if verbose:
		click.echo('Verbose mode activated')

@cli.command()
@click.argument('input', nargs=-1)
@click.option('--module', default='hi', help='select a module')
def say(input, module):
	''' Dudely Command line interface to help with daily tasks '''
	if input:
		click.echo('input = %s' % input)
	else:
		click.echo('no input specified')
	click.echo('You are in module = %s' % module)

@cli.command()
@click.argument('input', nargs=-1)
@click.option('--module', default='hi', help='select a module')
def dontsay(input, module):
	''' Dudely Command line interface to help with daily tasks '''
	click.echo('input = %s' % input)
	click.echo('You are in module = %s' % module)
