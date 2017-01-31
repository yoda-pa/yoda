import click
import chalk
import sys
from modules import *

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
	'''
	Helps with your git operations\n
	------------------------------\n
	Some commands that can be used:\n
	dude git all status  - goes into all repos in current directory and shows the status of all\n
	dude git credentials - shows your credentials. If not set, it would prompt for input\n
	dude git agenda      - Show all the repos worked on in the past and suggest which ones should be worked on depending on commits etc\n
	dude git push all    - Pushes everything with automatically generated commits (you will have the option to manually enter the commit messages before committing)\n
	re
	'''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
		data = sys.modules['modules.git'].process(test_string)
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
		data = sys.modules['modules.chat'].process(test_string)
	else:
		click.echo('No input specified. Run with --help for info')

# devtools
@cli.command()
@click.argument('input', nargs=-1)
def dev(input):
	''' dev tools '''
	if input:
		test_string = ''
		for i in input:
			test_string += (i + ' ')
		data = sys.modules['modules.dev'].process(test_string)
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
		data = sys.modules['modules.family'].process(test_string)
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
		data = sys.modules['modules.love'].process(test_string)
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
		data = sys.modules['modules.diary'].process(test_string)
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
		data = sys.modules['modules.money'].process(test_string)
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
		data = sys.modules['modules.study'].process(test_string)
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
		data = sys.modules['modules.health'].process(test_string)
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
		data = sys.modules['modules.learn'].process(test_string)
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
		data = sys.modules['modules.fashion'].process(test_string)
	else:
		click.echo('No input specified. Run with --help for info')
