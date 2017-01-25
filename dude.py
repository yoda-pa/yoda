import click

@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
	''' Dudely Command line interface to help with daily tasks '''
	if verbose:
		click.echo('Verbose mode activated')

# test
@cli.command()
@click.argument('input', nargs=-1)
def test(input):
	''' For testing new features '''
	if input:
		for i in input:
			click.echo('input = %s' % i)
	else:
		click.echo('no input specified')

# git
@cli.command()
@click.argument('input', nargs=-1)
def git(input):
	''' git '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# chat
@cli.command()
@click.argument('input', nargs=-1)
def chat(input):
	''' chat '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
		click.echo('input = %s' % test_string)
	else:
		click.echo('No input specified. Run with --help for info')

# devtools
@cli.command()
@click.argument('input', nargs=-1)
def devtools(input):
	''' devtools '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# family
@cli.command()
@click.argument('input', nargs=-1)
def family(input):
	''' family '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# love
@cli.command()
@click.argument('input', nargs=-1)
def love(input):
	''' love '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# diary
@cli.command()
@click.argument('input', nargs=-1)
def diary(input):
	''' diary '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# money
@cli.command()
@click.argument('input', nargs=-1)
def money(input):
	''' money '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# study
@cli.command()
@click.argument('input', nargs=-1)
def study(input):
	''' study '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# health
@cli.command()
@click.argument('input', nargs=-1)
def health(input):
	''' health '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# learn
@cli.command()
@click.argument('input', nargs=-1)
def learn(input):
	''' learn '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')

# fashion
@cli.command()
@click.argument('input', nargs=-1)
def fashion(input):
	''' fashion '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
	else:
		click.echo('No input specified. Run with --help for info')
