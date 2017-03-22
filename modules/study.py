import click
import chalk

def vocabulary():
    words = {}
    with open('resources/vocab-words.txt') as fp:
        for line in fp.read().split('\n'):
            line = line.strip()
            if len(line) > 0:
                (word, definition) = line.split(' - ')
                words[word.lower().strip()] = definition.strip()
    print(words)

# command checker
def check_sub_command(c):
    sub_commands = {
        'vocab' : vocabulary
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude learn --help" for more info')

# the main process
def process(input):
    input = input.lower().strip()
    check_sub_command(input)
