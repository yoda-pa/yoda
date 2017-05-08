import click
import chalk
import random
from util import *
from config import config_file_paths
import time
import datetime
import requests
# the main process


@click.group()
def learn():
    """
        The learn module
    """

# ----------------------- / vocabulary code -----------------------#


# config file path
VOCABULARY_CONFIG_FILE_PATH = config_file_paths["VOCABULARY_CONFIG_FILE_PATH"]
VOCABULARY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    VOCABULARY_CONFIG_FILE_PATH)

# getting words
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
    # TODO: process result data and get word depending on the history of it too
    click.echo(click.style(word + ": ", bold=True))
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
    create_folder(VOCABULARY_CONFIG_FOLDER_PATH)
    with open(VOCABULARY_CONFIG_FOLDER_PATH + '/results.txt', 'a') as fp:
        timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fp.write('{} {} {}\n'.format(timestamp, word, correct))

# calculates accuracy


def get_word_accuracy_of_previous_words():
    accuracy = {}
    for word in words:
        accuracy[word] = []
    if not os.path.isfile(VOCABULARY_CONFIG_FOLDER_PATH + '/results.txt'):
        chalk.red(
            'No words learned in the past. Please use "dude vocabulary word" for the same')
        return
    with open(VOCABULARY_CONFIG_FOLDER_PATH + '/results.txt') as fp:
        for line in fp.read().split('\n'):
            if len(line) == 0:
                continue
            (date, time, word, correct) = line.split()
            correct = int(correct)
            if word in accuracy:
                accuracy[word].append(correct)

    words_in_history = {}

    for word, lst in accuracy.items():
        if len(lst):
            words_in_history[word] = []
            words_in_history[word].append(len(lst))
            words_in_history[word].append(
                round((sum(lst) * 100) / len(lst)) if len(lst) else 0)

    click.echo(click.style("Words asked in the past: ", bold=True))
    # print(words_in_history)
    for word, ar in words_in_history.items():
        click.echo(word + '-- times used: ' +
                   str(ar[0]) + ' accuracy: ' + str(ar[1]))

# command checker


def check_sub_command_vocab(c):
    sub_commands = {
        'word': random_word,
        'accuracy': get_word_accuracy_of_previous_words
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
# config file path
FLASHCARDS_CONFIG_FILE_PATH = config_file_paths["FLASHCARDS_CONFIG_FILE_PATH"]
FLASHCARDS_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    FLASHCARDS_CONFIG_FILE_PATH)

def get_selected_set():
    if os.path.isfile(FLASHCARDS_CONFIG_FOLDER_PATH + '/selected_study_set'):
        with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/selected_study_set') as fp:
            lines = fp.read().split('\n')
            return lines[0].strip()

SELECTED_STUDY_SET = get_selected_set()
# ----- functions for sets -----


def get_set_statuses():
    sets = {}
    if not os.path.isfile(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt'):
        return None
    with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt') as fp:
        for line in fp.read().split('\n'):
            line = line.strip()
            if len(line) > 0:
                (name, is_open, description) = line.split('-')
                sets[name.lower().strip()] = int(is_open)
    return sets


def get_set_descriptions():
    sets = {}
    if not os.path.isfile(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt'):
        return None
    with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt') as fp:
        for line in fp.read().split('\n'):
            line = line.strip()
            if len(line) > 0:
                (name, is_open, description) = line.split('-')
                sets[name.lower().strip()] = description
    return sets

# gives you a list of all the study sets


def list_sets_fc(dummy):
    sets = get_set_statuses()
    descriptions = get_set_descriptions()
    if not sets:
        chalk.red(
            'There are no sets right now. Type "dude flashcards sets new <name>" to create one')
    else:
        i = 0
        there_are_sets = False
        for set in sets:
            if sets[set] >= 1:
                if not there_are_sets:
                    click.echo('List of all the study sets:')
                    there_are_sets = True
                i += 1
                click.echo(str(i) + ') ' + set)
        if not there_are_sets:
            chalk.red(
                'Looks like all the sets are closed. Please create a new one or open an existing one')

# creates new study set


def new_set_fc(name):
    if name:
        if len(name.split()) > 1:
            chalk.red('The length of name should not be more than one')
        else:
            sets = get_set_statuses()
            if not sets:
                # there is no file, so create one
                create_folder(FLASHCARDS_CONFIG_FOLDER_PATH)

                description = raw_input('Enter a description:\n')

                with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt', 'a') as fp:
                    fp.write('{}-{}-{}\n'.format(name, 1, description))
            else:
                # assuming that the set exists. if it doesn't, catch
                try:
                    if (sets[name] != 0 and sets[name] != 1):
                        chalk.red('Set already exists')
                except KeyError:
                    create_folder(FLASHCARDS_CONFIG_FOLDER_PATH)

                    description = raw_input('Enter a description:\n')

                    with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt', 'a') as fp:
                        fp.write('{}-{}-{}\n'.format(name, 1, description))
                    chalk.red('Set added')
    else:
        chalk.red('Please enter the name of new study set after the command')


def modify_set_fc_util(name, new_name):
    sets = get_set_statuses()
    descriptions = get_set_descriptions()
    # delete existing file
    os.remove(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt')
    for set in sets:
        with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt', 'a') as fp:
            fp.write('{} {}\n'.format(set if set !=
                                      name else new_name, sets[set]))


def modify_set_fc_description(name, new_name):
    descriptions = get_set_descriptions()
    # delete existing file
    os.remove(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt')
    for set in sets:
        with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/sets.txt', 'a') as fp:
            fp.write('{}-{}-{}\n'.format(set if set !=
                                         name else new_name, sets[set], ))

# modify a set


def modify_set_fc(name):
    sets = get_set_statuses()
    if not sets:
        chalk.red(
            'There are no sets right now. Type "dude flashcards sets new <name>" to create one')
    else:
        if not sets[name]:
            chalk.red('There is no set named ' + name + '.')
        else:
            chalk.blue(
                'Edit a new name for this set: (If you wish to keep it the same, just type a single \'-\' without the quotes)')
            new_name = raw_input().strip()
            if not (new_name == None or new_name == '-' or new_name == ''):
                modify_set_fc_name(name, new_name)
                modify_set_fc_description(name, new_name)
                print('The name was modified from \'' +
                      name + '\' to \'' + new_name + '\'')

# select working study set


def select_set_fc(name):
    sets = get_set_statuses()
    descriptions = get_set_descriptions()
    if not sets:
        chalk.red(
            'There are no sets right now. Type "dude flashcards sets new <name>" to create one')
    else:
        try:
            if sets[name] == 0:
                chalk.red(
                    'Looks like the study set you want to select is closed. Please modify it first')
            elif sets[name] == 1:
                SELECTED_STUDY_SET = name
                with open(FLASHCARDS_CONFIG_FOLDER_PATH + '/selected_study_set', 'w') as fp:
                    fp.write(SELECTED_STUDY_SET)
                chalk.blue('Selected study set: ' + SELECTED_STUDY_SET)
        except KeyError:
            chalk.red('Set does not exist')
# command checker flashcards sets


def check_sub_command_sets_flashcards(c, name):
    sub_commands = {
        'list': list_sets_fc,
        'new': new_set_fc,
        'modify': modify_set_fc,
        'select': select_set_fc
    }
    # try:
    return sub_commands[c](name)
    # except KeyError:
    #     chalk.red('Command does not exist!')
    #     click.echo('Try "dude flashcards --help" for more info')
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
        'add': add_card_fc,
        'modify': modify_cards_fc
    }
    try:
        return sub_commands[c](name)
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude flashcards --help" for more info')
# ----- / functions for cards -----


def status_fc(set, dummy):
    if not SELECTED_STUDY_SET:
        chalk.red('No set selected')
    else:
        description = get_set_descriptions()[SELECTED_STUDY_SET]
        click.echo('Selected set: ' + SELECTED_STUDY_SET)
        click.echo('Description: ' + description)


def study_fc(set, dummy):
    print('study set: ' + set)
    # if no set is specified, study selected set.
    # if no selected, panic!


@learn.command()
@click.argument('domain', nargs=1)
@click.argument('action', nargs=1, required=False)
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
        \t \t select <name>: select an existing study set\n
        \t cards: Flash cards\n
        \t \t Actions:\n
        \t \t add <name>: add a flashcard to the working study set\n
        \t \t modify: modify cards in the selected study set\n
        \t status: Current status of study study set
        \t study: start studying a study set
    """
    domain = str(domain)
    action = str(action)
    name = tuple_to_string(name)
    domains = {
        'cards': check_sub_command_cards_flashcards,
        'sets': check_sub_command_sets_flashcards,
        'status': status_fc,
        'study': study_fc
    }
    # try:
    domains[domain](action, name)
    # except KeyError:
    #     chalk.red('Command does not exist!')
    #     click.echo('Try "dude flashcards --help" for more info')
# ----------------------- / flashcards code -----------------------#


@learn.command()
@click.argument('word', nargs=1)
def define(word):
    """
        Get the meaning of a word
    """
    word = str(word)
    r = requests.get('https://wordsapiv1.p.mashape.com/words/' + word + '/definitions', headers={
        'X-Mashape-Key': 'Yq72o8odIlmshPTjxnTMN1xixyy5p1lgtd0jsn2NsJfn7pflhR',
        "Accept": "application/json"
    })
    data = r.json()    #output['output'] = TextTemplate('Definition of ' + word + ':\n' + data['definitions'][0]['definition']).get_message()

    try:
        word = data['word']
        posted = False
        if len(data['definitions']):
            if not posted:
                chalk.blue('A few definitions of the word "' + word + '" with their parts of speech are given below:')
                click.echo('---------------------------------')
                posted = True

            for definition in data['definitions']:
                print(definition['partOfSpeech'] + ': ' + definition['definition'])

        # if this word is not in the vocabulary list, add to it!
        if posted:
            words = get_words_list()
            if word in words:
                chalk.blue('This word already exists in the vocabulary set, so you can practice it while using that')
            else:
                with open('resources/vocab-words.txt', 'a') as fp:
                    fp.write('{} - {}\n'.format(word, data['definitions'][0]['definition']))
                chalk.blue('This word does not exist in the vocabulary set, so it has been added to it so that you can practice it while using that')
        else:
            chalk.red('Sorry, no definitions were found for this word')
    except KeyError:
        chalk.red('Sorry, no definitions were found for this word')
