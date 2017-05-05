import click
import chalk
import random
from util import *
from config import config_file_paths
import time
import datetime

# config file path
LEARN_CONFIG_FILE_PATH = config_file_paths["LEARN_CONFIG_FILE_PATH"]
LEARN_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(LEARN_CONFIG_FILE_PATH)

# the main process
@click.group()
def learn():
    """
        The learn module
    """

# ----------------------- / vocabulary code -----------------------#
words = {}
with open('resources/vocab-words.txt') as fp:
    for line in fp.read().split('\n'):
        line = line.strip()
        if len(line) > 0:
            (word, definition) = line.split(' - ')
            words[word.lower().strip()] = definition.strip()

def get_words_list():
    return words

# displays a random word
def random_word():
    words = get_words_list()
    word, meaning = random.choice(words.items())
    click.echo(click.style(word + ": ", bold = True))
    raw_input('<Enter> to show meaning')
    click.echo(meaning)

    # check if the user knows about this word or not
    result = raw_input('Did you know / remember the meaning?\n')
    correct = 0
    incorrect = 0
    if result == 'y' or result == 'yes':
        correct = 1
    else:
        incorrect = 1
    create_folder(LEARN_CONFIG_FOLDER_PATH)
    with open(LEARN_CONFIG_FOLDER_PATH + '/results.txt', 'a') as fp:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fp.write('{} {} {}\n'.format(timestamp, word, correct))

def get_word_accuracy_of_previous_words():
    accuracy = {}
    for word in words:
        accuracy[word] = []
    with open(LEARN_CONFIG_FOLDER_PATH + '/results.txt') as fp:
        for line in fp.read().split('\n'):
            if len(line) == 0: continue
            (date, time, word, correct) = line.split()
            correct = int(correct)
            if word in accuracy:
                accuracy[word].append(correct)

    words_in_history = {}

    for word, lst in accuracy.items():
        if len(lst):
            words_in_history[word] = []
            words_in_history[word].append(len(lst))
            words_in_history[word].append(round((sum(lst) * 100)/len(lst)) if len(lst) else 0)

    click.echo(click.style("Words asked in the past: ", bold = True))
    # print(words_in_history)
    for word, ar in words_in_history.items():
        click.echo(word + '-- times used: ' + str (ar[0]) + ' accuracy: ' + str(ar[1]))

# command checker
def check_sub_command_vocab(c):
    sub_commands = {
        'word' : random_word,
        'accuracy' : get_word_accuracy_of_previous_words
    }
    try:
        return sub_commands[c]()
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude setup --help" for more info')

@learn.command()
@click.argument('input', nargs=-1)
def vocabulary(input):
    """
        For enhancing your vocabulary and tracking your progress\n\n
    	Commands:\n
    	word: get a random word\n
    	accuracy: view your progress
    """
    input = tuple_to_string(input)
    check_sub_command_vocab(input)
# ----------------------- / vocabulary code -----------------------#


# ----------------------- flashcards code -----------------------#
# ----- functions for sets -----
def list_sets_fc(dummy):
    print('list sets')

def new_set_fc(name):
    if name:
        if len(name.split()) > 1:
            chalk.red('The length of name should not be more than one')
        else:
            # here
            print('new set ' + name)
    else:
        chalk.red('Please enter the name of new study set after the command')

def modify_set_fc(name):
    print('modify set ' + name)

# command checker flashcards sets
def check_sub_command_sets_flashcards(c, name):
    sub_commands = {
        'list' : list_sets_fc,
        'new' : new_set_fc,
        'modify' : modify_set_fc
    }
    try:
        return sub_commands[c](name)
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude flashcards --help" for more info')
# ----- / functions for sets -----

# ----- functions for cards -----
def add_card_fc(name):
    print('add card ' + name)

def modify_cards_fc(dummy):
    # we will show all cards and ask which one to modify
    print('modify cards')

# command checker flashcards cards
def check_sub_command_cards_flashcards(c, name):
    sub_commands = {
        'add' : add_card_fc,
        'modify' : modify_cards_fc
    }
    try:
        return sub_commands[c](name)
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude flashcards --help" for more info')
# ----- / functions for cards -----

def status_fc(set, dummy):
    print('selected set: ' + set)

def study_fc(set, dummy):
    print('study set: ' + set)
    # if no set is specified, study selected set.
    # if no selected, panic!

@learn.command()
@click.argument('domain', nargs=1)
@click.argument('action', nargs=1)
@click.argument('name', nargs=-1, required=False)
def flashcards(domain, action, name):
    """
        Flashcards for learning anything and tracking your progress\n\n
        Domains:\n
        \t sets: Study sets\n
        \t \t Actions:\n
        \t \t list: view study sets\n
        \t \t new <name>: create a new study set\n
        \t \t modify <name>: modify a study set\n
        \t cards: Flash cards\n
        \t \t Actions:\n
        \t \t add <name>: add a flashcard to the working study set\n
        \t \t modify: modify cards in the selected study set\n
        \t select: select an existing study set\n
        \t study: start studying a study set
    """
    domain = str(domain)
    action = str(action)
    name = tuple_to_string(name)
    domains = {
        'cards' : check_sub_command_cards_flashcards,
        'sets' : check_sub_command_sets_flashcards,
        'status' : status_fc,
        'study' : study_fc
    }
    try:
        domains[domain](action, name)
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude flashcards --help" for more info')
# ----------------------- / flashcards code -----------------------#
