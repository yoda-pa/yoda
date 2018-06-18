from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import random
import sys
import time
from builtins import str

import requests
from collections import defaultdict
from os import listdir
from past.utils import old_div

from .config import get_config_file_paths
from .util import *


# the main process


@click.group()
def learn():
    """
        The learn module
    """


# ----------------------- / vocabulary code -----------------------#


# config file path
def get_vocabulary_config_file_path():
    return get_config_file_paths()["VOCABULARY_CONFIG_FILE_PATH"]

def get_vocabulary_config_folder_path():
    return get_folder_path_from_file_path(
    get_vocabulary_config_file_path())


def get_words(package='yoda', resource='resources/vocab-words.txt'):
    """
    Get words to learn. Each key in dict represent word to learn, values represent definition.

    :return: words
    :rtype: dict
    """
    words = {}
    path = os.path.dirname(sys.modules[package].__file__)

    with open(os.path.join(path, resource), 'r') as f:
        data = f.read()

    for line in data.split('\n'):
        line = line.strip()
        if len(line) > 0:
            (word, definition) = line.split(' - ')
            words[word.lower().strip()] = definition.strip()
    return words


def calculate_weight(correct, total):
    return correct + total * 0.5


def get_weights():
    """
    Calculate weights for a set of words based on past results.
    :return: dict (word -> weight)
    """
    accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
    words = get_words()
    with open(get_vocabulary_config_folder_path() + '/results.txt') as fp:
        for _line in fp.read().split('\n'):
            if len(_line) == 0:
                continue
            (date, _time, _word, correct) = _line.split()
            correct = int(correct)
            accuracy[_word]['correct'] += correct
            accuracy[_word]['total'] += 1

    for word in words.keys():
        words[word] = calculate_weight(**accuracy[word])
    return words


def get_accuracy_percentage():
    accuracy = defaultdict(list)
    with open(get_vocabulary_config_folder_path() + '/results.txt') as fp:
        for _line in fp.read().split('\n'):
            if len(_line) == 0:
                continue
            (date, _time, _word, correct) = _line.split()
            correct = int(correct)
            accuracy[_word].append(correct)

    words_in_history = {}

    for _word, lst in list(accuracy.items()):
        if len(lst):
            words_in_history[_word] = []
            words_in_history[_word].append(len(lst))
            words_in_history[_word].append(
                round(old_div((sum(lst) * 100), len(lst))) if len(lst) else 0)
    return words_in_history


def get_word_to_learn():
    # in case no results is yet available pick random word
    if not os.path.isfile(get_vocabulary_config_folder_path() + '/results.txt'):
        return random.choice(list(get_words().keys()))
    words = get_weights()
    return sorted(words, key=words.get, reverse=True).pop()


def pick_word():
    """
    Picks and tests user for definition of word.
    """
    meanings = get_words()
    word = get_word_to_learn()
    meaning = meanings[word]

    click.echo(click.style(word + ": ", bold=True))
    input('<Enter> to show meaning')
    click.echo(meaning)

    # check if the user knows about this word or not
    result = input('Did you know / remember the meaning?\n')
    correct = 0
    if result == 'y' or result == 'yes':
        correct = 1
    create_folder(get_vocabulary_config_folder_path())
    with open(get_vocabulary_config_folder_path() + '/results.txt', 'a') as fp:
        timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fp.write('{} {} {}\n'.format(timestamp, word, correct))


def display_word_accuracy():
    """
    Calculates and displays users accuracy.
    """
    if not os.path.isfile(get_vocabulary_config_folder_path() + '/results.txt'):
        click.echo(chalk.red(
            'No words learned in the past. Please use "yoda vocabulary word" for the same'))
        return

    words = get_accuracy_percentage()

    click.echo(click.style("Words asked in the past: ", bold=True))
    for _word, ar in list(words.items()):
        click.echo(_word + '-- times used: ' +
                   str(ar[0]) + ' accuracy: ' + str(ar[1]))


def display_word_weights():
    """
    Displays word weights.
    """
    if not os.path.isfile(get_vocabulary_config_folder_path() + '/results.txt'):
        click.echo(chalk.red(
            'No words learned in the past. Please use "yoda vocabulary word" for the same'))
        return

    words = get_weights()

    click.echo(click.style("Words asked in the past: ", bold=True))
    for _word, ar in list(words.items()):
        click.echo('{0} -- weight: {1}'.format(_word, str(ar)))


def check_sub_command_vocab(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        'word': pick_word,
        'accuracy': display_word_accuracy,
        'weights': display_word_weights,
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda vocabulary --help" for more info')


@learn.command()
@click.pass_context
@click.argument('input', nargs=-1, required=False, callback=alias_checker)
def vocabulary(ctx, input):
    """
        For enhancing your vocabulary and tracking your progress\n\n
        Commands:\n
        word: get a random word\n
        accuracy: view your progress
    """
    arguments = get_arguments(ctx, -1)
    _input = tuple_to_string(arguments)
    check_sub_command_vocab(_input)


# ----------------------- / vocabulary code -----------------------#


# ----------------------- flashcards code -----------------------#
# config file path
def get_flashcards_config_file_path():
    return get_config_file_paths()["FLASHCARDS_CONFIG_FILE_PATH"]

def get_flashcards_config_folder_path():
    return get_folder_path_from_file_path(
        get_flashcards_config_file_path())


def get_selected_set():
    """
    get selected set
    :return:
    """
    if os.path.isfile(get_flashcards_config_folder_path() + '/selected_study_set'):
        with open(get_flashcards_config_folder_path() + '/selected_study_set') as fp:
            lines = fp.read().split('\n')
            return lines[0].strip()


SELECTED_STUDY_SET = get_selected_set()


# ----- functions for sets -----


def get_set_statuses():
    sets = {}
    if not os.path.isfile(get_flashcards_config_folder_path() + '/sets.txt'):
        return None
    with open(get_flashcards_config_folder_path() + '/sets.txt') as fp:
        for _line in fp.read().split('\n'):
            _line = _line.strip()
            if len(_line) > 0:
                (name, is_open, description) = _line.split('-')
                sets[name.lower().strip()] = int(is_open)
    return sets


def get_set_descriptions():
    """
    get description of sets
    :return:
    """
    sets = {}
    if not os.path.isfile(get_flashcards_config_folder_path() + '/sets.txt'):
        return None
    with open(get_flashcards_config_folder_path() + '/sets.txt') as fp:
        for _line in fp.read().split('\n'):
            _line = _line.strip()
            if len(_line) > 0:
                (name, is_open, description) = _line.split('-')
                sets[name.lower().strip()] = description
    return sets


def list_sets_fc(dummy):
    """
    gives you a list of all the study sets
    :param dummy:
    """
    sets = get_set_statuses()
    if not sets:
        click.echo(chalk.red(
            'There are no sets right now. Type "yoda flashcards sets new <name>" to create one'))
    else:
        i = 0
        there_are_sets = False
        for _set in sets:
            if sets[_set] >= 1:
                if not there_are_sets:
                    click.echo('List of all the study sets:')
                    there_are_sets = True
                i += 1
                click.echo(str(i) + ') ' + _set)
        if not there_are_sets:
            click.echo(chalk.red(
                'Looks like all the sets are closed. Please create a new one or open an existing one'))


def new_set_fc(name):
    """
    creates new study set
    :param name:
    """
    if name:
        if len(name.split()) > 1:
            click.echo(chalk.red('The length of name should not be more than one'))
        else:
            sets = get_set_statuses()
            if not sets:
                # there is no file, so create one
                create_folder(get_flashcards_config_folder_path())

                description = input('Enter a description:\n')

                with open(get_flashcards_config_folder_path() + '/sets.txt', 'a') as fp:
                    fp.write('{}-{}-{}\n'.format(name, 1, description))
            else:
                # assuming that the set exists. if it doesn't, catch
                try:
                    if sets[name] != 0 and sets[name] != 1:
                        click.echo(chalk.red('Set already exists'))
                except KeyError:
                    create_folder(get_flashcards_config_folder_path())

                    description = input('Enter a description:\n')

                    with open(get_flashcards_config_folder_path() + '/sets.txt', 'a') as fp:
                        fp.write('{}-{}-{}\n'.format(name, 1, description))

                    # create folder for the set to add cards to it
                    create_folder(get_flashcards_config_folder_path() + '/' + name)

                    click.echo(chalk.red('Set added'))
    else:
        click.echo(chalk.red('Please enter the name of new study set after the command'))


def modify_set_fc_name(name, new_name):
    """
    util function
    :param name:
    :param new_name:
    """
    sets = get_set_statuses()
    # delete existing file
    os.remove(get_flashcards_config_folder_path() + '/sets.txt')
    for _set in sets:
        with open(get_flashcards_config_folder_path() + '/sets.txt', 'a') as fp:
            fp.write('{} {}\n'.format(_set if _set != name else new_name, sets[_set]))


def modify_set_fc_description(name, new_name):
    """
    modify description of a set
    :param name:
    :param new_name:
    """
    sets = get_set_statuses()
    # delete existing file
    os.remove(get_flashcards_config_folder_path() + '/sets.txt')
    for _set in sets:
        with open(get_flashcards_config_folder_path() + '/sets.txt', 'a') as fp:
            fp.write('{}-{}-{}\n'.format(_set if _set != name else new_name, sets[_set], ))


def modify_set_fc(name):
    """
    modify a set
    :param name:
    """
    sets = get_set_statuses()
    if not sets:
        click.echo(chalk.red(
            'There are no sets right now. Type "yoda flashcards sets new <name>" to create one'))
    else:
        if not sets[name]:
            click.echo(chalk.red('There is no set named ' + name + '.'))
        else:
            click.echo(chalk.blue(
                'Edit a new name for this set: (If you wish to keep it the same, just type a single \'-\' without the '
                'quotes)'))
            new_name = input().strip()
            if not (new_name is None or new_name == '-' or new_name == ''):
                modify_set_fc_name(name, new_name)
                modify_set_fc_description(name, new_name)
                print('The name was modified from \'' +
                      name + '\' to \'' + new_name + '\'')


def select_set_fc(name, dummy=None):
    """
    select working study set
    :param name:
    :param dummy:
    """
    sets = get_set_statuses()
    if not sets:
        click.echo(chalk.red(
            'There are no sets right now. Type "yoda flashcards sets new <name>" to create one'))
    else:
        try:
            if sets[name] == 0:
                click.echo(chalk.red(
                    'Looks like the study set you want to select is closed. Please modify it first'))
            elif sets[name] == 1:
                SELECTED_STUDY_SET = name
                with open(get_flashcards_config_folder_path() + '/selected_study_set', 'w') as fp:
                    fp.write(SELECTED_STUDY_SET)
                click.echo(chalk.blue('Selected study set: ' + SELECTED_STUDY_SET))
        except KeyError:
            click.echo(chalk.red('Set does not exist'))


def check_sub_command_sets_flashcards(c, name):
    """
    command checker flashcards sets
    :param c:
    :param name:
    :return:
    """
    sub_commands = {
        'list': list_sets_fc,
        'new': new_set_fc,
        'modify': modify_set_fc,
        'select': select_set_fc
    }
    try:
        return sub_commands[c](name)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda flashcards --help" for more info')


# ----- / functions for sets -----

# ----- functions for cards -----


def add_card_fc(name):
    """
    add flash card
    :param name:
    """
    SELECTED_STUDY_SET = get_selected_set()
    if SELECTED_STUDY_SET:
        print('add card "' + name + '"')
        print('Add description: (press Enter twice to stop)')
        x = input().strip()
        description = x
        while len(x):
            x = input().strip()
            description += ('\n' + x)

        description = description.strip()
        create_folder(get_flashcards_config_folder_path() + '/' + SELECTED_STUDY_SET)

        filename = spaces_to_colons(''.join(e for e in name if (e.isalnum() or e == ' ')))

        with open(get_flashcards_config_folder_path() + '/' + SELECTED_STUDY_SET + '/' + filename + '.txt', 'a') as fp:
            fp.write(colons_to_spaces(filename) + '\n')
            fp.write(description)
    else:
        click.echo(chalk.red('No set selected'))


def check_sub_command_cards_flashcards(c, name):
    """
    command checker flashcards cards
    :param c:
    :param name:
    :return:
    """
    sub_commands = {
        'add': add_card_fc
    }
    try:
        return sub_commands[c](name)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda flashcards --help" for more info')


# ----- / functions for cards -----


def status_fc(set, dummy):
    """
    flashcard status
    :param set:
    :param dummy:
    """
    SELECTED_STUDY_SET = get_selected_set()

    if not SELECTED_STUDY_SET:
        click.echo(chalk.red('No set selected'))
    else:
        description = get_set_descriptions()[SELECTED_STUDY_SET]
        click.echo('Selected set: ' + SELECTED_STUDY_SET)
        click.echo('Description: ' + description)
        if os.path.isdir(get_flashcards_config_folder_path() + '/' + SELECTED_STUDY_SET):
            cards_in_selected_set = str(len(listdir(get_flashcards_config_folder_path() + '/' + SELECTED_STUDY_SET)))
            click.echo('No. of cards in selected set: ' + cards_in_selected_set)
        else:
            click.echo('There are no cards in selected set ')


def study_fc(set, dummy):
    """
    start studying a set
    :param set:
    :param dummy:
    """

    if not SELECTED_STUDY_SET:
        click.echo(chalk.red('No set selected'))
    else:
        description = get_set_descriptions()[SELECTED_STUDY_SET]
        click.echo('Selected set: ' + SELECTED_STUDY_SET)
        click.echo('Description: ' + description)
        cards_in_selected_set = listdir(get_flashcards_config_folder_path() + '/' + SELECTED_STUDY_SET)
        len_cards_in_selected_set = len(cards_in_selected_set)
        width = get_terminal_width()
        if len_cards_in_selected_set == 0:
            click.echo(chalk.red('There are no cards in this set!'))
        else:
            i = 0
            click.echo(chalk.blue('Cards:'))
            click.echo(chalk.blue('_' * width))
            for card in cards_in_selected_set:
                i += 1

                card_path = get_flashcards_config_folder_path() + '/' + SELECTED_STUDY_SET + '/' + card
                with open(card_path) as fp:
                    name = None
                    description = ''
                    for line in fp.read().split('\n'):
                        line = line.strip()
                        if not name:
                            name = line
                        else:
                            description += (line + '\n')
                description = description.strip()
                if i > 0:
                    click.echo('-' * width)
                click.echo(str(i) + ': ' + name)
                click.echo('=' * width)
                click.echo(description)
                click.echo('=' * width)
                if i < len_cards_in_selected_set:
                    input('Press Enter to continue to next card')

@learn.command()
@click.pass_context
@click.argument('domain', nargs=1, required=False, callback=alias_checker)
@click.argument('action', nargs=1, required=False, callback=alias_checker)
@click.argument('name', nargs=-1, required=False, callback=alias_checker)
def flashcards(ctx, domain, action, name):
    domain, action, name = get_arguments(ctx, 3)
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
        \t status: Current status of study study set
        \t study: start studying the selected study set
    """
    domain = str(domain)
    action = str(action)
    name = tuple_to_string(name)
    domains = {
        'cards': check_sub_command_cards_flashcards,
        'sets': check_sub_command_sets_flashcards,
        'status': status_fc,
        'study': study_fc,
        'select': select_set_fc
    }
    try:
        domains[domain](action, name)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda flashcards --help" for more info')


# ----------------------- / flashcards code -----------------------#

# ----------------------- define code -----------------------#
@learn.command()
@click.pass_context
@click.argument('word', nargs=1, required=False, callback=alias_checker)
def define(ctx, word):
    """
        Get the meaning of a word
    """
    word = get_arguments(ctx, 1)
    _word = str(word)
    r = requests.get('https://wordsapiv1.p.mashape.com/words/' + _word + '/definitions', headers={
        'X-Mashape-Key': 'Yq72o8odIlmshPTjxnTMN1xixyy5p1lgtd0jsn2NsJfn7pflhR',
        "Accept": "application/json"
    })
    data = r.json()

    try:
        _word = data['word']
        posted = False
        if len(data['definitions']):
            if not posted:
                click.echo(chalk.blue(
                    'A few definitions of the word "' + _word + '" with their parts of speech are given below:'))
                click.echo('---------------------------------')
                posted = True

            for definition in data['definitions']:
                print(definition['partOfSpeech'] + ': ' + definition['definition'])

        # if this word is not in the vocabulary list, add to it!
        if posted:
            words = get_words_list()
            if _word in words:
                click.echo(chalk.blue(
                    'This word already exists in the vocabulary set, so you can practice it while using that'))
            else:
                with open('resources/vocab-words.txt', 'a') as fp:
                    fp.write('{} - {}\n'.format(_word, data['definitions'][0]['definition']))
                click.echo(chalk.blue(
                    'This word does not exist in the vocabulary set, so it has been added to it so that you can '
                    'practice it while using that'))
        else:
            click.echo(chalk.red('Sorry, no definitions were found for this word'))
    except KeyError:
        click.echo(chalk.red('Sorry, no definitions were found for this word'))
        print('Sorry, no definitions were found for this word')

# ----------------------- / define code -----------------------#
