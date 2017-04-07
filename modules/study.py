import click
import chalk
import random
from util import *
from config import config_file_paths
import time
import datetime

# config file path
STUDY_CONFIG_FILE_PATH = config_file_paths["STUDY_CONFIG_FILE_PATH"]
STUDY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(STUDY_CONFIG_FILE_PATH)

# the main process
@click.group()
def study():
    """
        The study module
    """

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
    result = raw_input('Did you know remember the meaning?\n')
    correct = 0
    incorrect = 0
    if result == 'y' or result == 'yes':
        correct = 1
    else:
        incorrect = 1
    create_folder(STUDY_CONFIG_FOLDER_PATH)
    with open(STUDY_CONFIG_FOLDER_PATH + '/results.txt', 'a') as fp:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fp.write('{} {} {}\n'.format(timestamp, word, correct))

def get_word_accuracy_of_previous_words():
    accuracy = {}
    for word in words:
        accuracy[word] = []
    with open(STUDY_CONFIG_FOLDER_PATH + '/results.txt') as fp:
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

@study.command()
@click.argument('input', nargs=-1)
def vocabulary(input):
    """
        Helps you in vocab
    """
    input = tuple_to_string(input)
    check_sub_command_vocab(input)
