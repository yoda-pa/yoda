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


# Constants:
VOCAB_LIST = "resources/vocab-words.txt"

# the main process


@click.group()
def learn():
    """
        The learn module
    """


# ----------------------- / vocabulary code -----------------------#


# config file path
VOCABULARY_CONFIG_FILE_PATH = get_config_file_paths()["VOCABULARY_CONFIG_FILE_PATH"]
VOCABULARY_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    VOCABULARY_CONFIG_FILE_PATH
)


def get_words(package="yoda", resource=VOCAB_LIST):
    """
    Get words to learn. Each key in dict represent word to learn, values represent definition.

    :return: words
    :rtype: dict
    """
    words = {}
    path = os.path.dirname(sys.modules[package].__file__)

    with open(os.path.join(path, resource), "r") as f:
        data = f.read()

    for line in data.split("\n"):
        line = line.strip()
        if len(line) > 0:
            (word, definition) = line.split(" - ")
            words[word.lower().strip()] = definition.strip()
    return words


def calculate_weight(correct, total):
    return correct + total * 0.5


def get_weights():
    """
    Calculate weights for a set of words based on past results.
    :return: dict (word -> weight)
    """
    accuracy = defaultdict(lambda: {"correct": 0, "total": 0})
    words = get_words()
    with open(VOCABULARY_CONFIG_FOLDER_PATH + "/results.txt") as fp:
        for _line in fp.read().split("\n"):
            if len(_line) == 0:
                continue
            (date, _time, _word, correct) = _line.split()
            correct = int(correct)
            accuracy[_word]["correct"] += correct
            accuracy[_word]["total"] += 1

    for word in words.keys():
        words[word] = calculate_weight(**accuracy[word])
    return words


def get_accuracy_percentage():
    accuracy = defaultdict(list)
    with open(VOCABULARY_CONFIG_FOLDER_PATH + "/results.txt") as fp:
        for _line in fp.read().split("\n"):
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
                round(old_div((sum(lst) * 100), len(lst))) if len(lst) else 0
            )
    return words_in_history


def get_word_to_learn():
    # in case no results is yet available pick random word
    if not os.path.isfile(VOCABULARY_CONFIG_FOLDER_PATH + "/results.txt"):
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
    input("<Enter> to show meaning")
    click.echo(meaning)

    # check if the user knows about this word or not
    result = input("Did you know / remember the meaning?\n")
    correct = 0
    if result == "y" or result == "yes":
        correct = 1
    create_folder(VOCABULARY_CONFIG_FOLDER_PATH)
    with open(VOCABULARY_CONFIG_FOLDER_PATH + "/results.txt", "a") as fp:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        fp.write("{} {} {}\n".format(timestamp, word, correct))


def display_word_accuracy():
    """
    Calculates and displays users accuracy.
    """
    if not os.path.isfile(VOCABULARY_CONFIG_FOLDER_PATH + "/results.txt"):
        click.echo(
            chalk.red(
                'No words learned in the past. Please use "yoda vocabulary word" for the same'
            )
        )
        return

    words = get_accuracy_percentage()

    click.echo(click.style("Words asked in the past: ", bold=True))
    for _word, ar in list(words.items()):
        click.echo(_word + "-- times used: " + str(ar[0]) + " accuracy: " + str(ar[1]))


def display_word_weights():
    """
    Displays word weights.
    """
    if not os.path.isfile(VOCABULARY_CONFIG_FOLDER_PATH + "/results.txt"):
        click.echo(
            chalk.red(
                'No words learned in the past. Please use "yoda vocabulary word" for the same'
            )
        )
        return

    words = get_weights()

    click.echo(click.style("Words asked in the past: ", bold=True))
    for _word, ar in list(words.items()):
        click.echo("{0} -- weight: {1}".format(_word, str(ar)))


def check_sub_command_vocab(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        "word": pick_word,
        "accuracy": display_word_accuracy,
        "weights": display_word_weights,
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
        click.echo('Try "yoda vocabulary --help" for more info')


@learn.command()
@click.pass_context
@click.argument("input", nargs=-1, required=False, callback=alias_checker)
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
FLASHCARDS_CONFIG_FILE_PATH = get_config_file_paths()["FLASHCARDS_CONFIG_FILE_PATH"]
FLASHCARDS_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(
    FLASHCARDS_CONFIG_FILE_PATH
)


def get_selected_set():
    """
    get selected set
    :return:
    """
    if os.path.isfile(FLASHCARDS_CONFIG_FOLDER_PATH + "/selected_study_set"):
        with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/selected_study_set") as fp:
            lines = fp.read().split("\n")
            return lines[0].strip()


SELECTED_STUDY_SET = get_selected_set()


# ----- functions for sets -----


def get_set_statuses():
    sets = {}
    if not os.path.isfile(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt"):
        return None
    with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt") as fp:
        for _line in fp.read().split("\n"):
            _line = _line.strip()
            if len(_line) > 0:
                (name, is_open, description) = _line.split("-")
                sets[name.lower().strip()] = int(is_open)
    return sets


def get_set_descriptions():
    """
    get description of sets
    :return:
    """
    sets = {}
    if not os.path.isfile(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt"):
        return None
    with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt") as fp:
        for _line in fp.read().split("\n"):
            _line = _line.strip()
            if len(_line) > 0:
                (name, is_open, description) = _line.split("-")
                sets[name.lower().strip()] = description
    return sets


def list_sets_fc(dummy):
    """
    gives you a list of all the study sets
    :param dummy:
    """
    sets = get_set_statuses()
    if not sets:
        click.echo(
            chalk.red(
                'There are no sets right now. Type "yoda flashcards sets new <name>" to create one'
            )
        )
    else:
        there_are_sets = False
        for i, _set in enumerate(sets):
            if sets[_set] >= 1:
                if not there_are_sets:
                    click.echo("List of all the study sets:")
                    there_are_sets = True
                click.echo(str(i) + ") " + _set)
        if not there_are_sets:
            click.echo(
                chalk.red(
                    "Looks like all the sets are closed. Please create a new one or open an existing one"
                )
            )


def new_set_fc(name):
    """
    creates new study set
    :param name:
    """
    if name:
        if len(name.split()) > 1:
            click.echo(chalk.red("The length of name should not be more than one"))
        else:
            sets = get_set_statuses()
            if not sets:
                # there is no file, so create one
                create_folder(FLASHCARDS_CONFIG_FOLDER_PATH)

                description = input("Enter a description:\n")

                with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt", "a") as fp:
                    fp.write("{}-{}-{}\n".format(name, 1, description))
            else:
                # assuming that the set exists. if it doesn't, catch
                try:
                    if sets[name] != 0 and sets[name] != 1:
                        click.echo(chalk.red("Set already exists"))
                except KeyError:
                    create_folder(FLASHCARDS_CONFIG_FOLDER_PATH)

                    description = input("Enter a description:\n")

                    with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt", "a") as fp:
                        fp.write("{}-{}-{}\n".format(name, 1, description))

                    # create folder for the set to add cards to it
                    create_folder(FLASHCARDS_CONFIG_FOLDER_PATH + "/" + name)

                    click.echo(chalk.red("Set added"))
    else:
        click.echo(
            chalk.red("Please enter the name of new study set after the command")
        )


def modify_set_fc_name(name, new_name):
    """
    util function
    :param name:
    :param new_name:
    """
    sets = get_set_statuses()
    # delete existing file
    os.remove(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt")
    for _set in sets:
        with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt", "a") as fp:
            fp.write("{} {}\n".format(_set if _set != name else new_name, sets[_set]))


def modify_set_fc_description(name, new_name):
    """
    modify description of a set
    :param name:
    :param new_name:
    """
    sets = get_set_statuses()
    # delete existing file
    os.remove(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt")
    for _set in sets:
        with open(FLASHCARDS_CONFIG_FOLDER_PATH + "/sets.txt", "a") as fp:
            fp.write(
                "{}-{}-{}\n".format(_set if _set != name else new_name, sets[_set])
            )


def modify_set_fc(name):
    """
    modify a set
    :param name:
    """
    sets = get_set_statuses()
    if not sets:
        click.echo(
            chalk.red(
                'There are no sets right now. Type "yoda flashcards sets new <name>" to create one'
            )
        )
    else:
        if not sets[name]:
            click.echo(chalk.red("There is no set named " + name + "."))
        else:
            click.echo(
                chalk.blue(
                    "Edit a new name for this set: (If you wish to keep it the same, just type a single '-' without the "
                    "quotes)"
                )
            )
            new_name = input().strip()
            if not (new_name is None or new_name == "-" or new_name == ""):
                modify_set_fc_name(name, new_name)
                modify_set_fc_description(name, new_name)
                print("The name was modified from '" + name + "' to '" + new_name + "'")


def select_set_fc(name, dummy=None):
    """
    select working study set
    :param name:
    :param dummy:
    """
    sets = get_set_statuses()
    if not sets:
        click.echo(
            chalk.red(
                'There are no sets right now. Type "yoda flashcards sets new <name>" to create one'
            )
        )
    else:
        try:
            if sets[name] == 0:
                click.echo(
                    chalk.red(
                        "Looks like the study set you want to select is closed. Please modify it first"
                    )
                )
            elif sets[name] == 1:
                SELECTED_STUDY_SET = name
                with open(
                    FLASHCARDS_CONFIG_FOLDER_PATH + "/selected_study_set", "w"
                ) as fp:
                    fp.write(SELECTED_STUDY_SET)
                click.echo(chalk.blue("Selected study set: " + SELECTED_STUDY_SET))
        except KeyError:
            click.echo(chalk.red("Set does not exist"))


def check_sub_command_sets_flashcards(c, name):
    """
    command checker flashcards sets
    :param c:
    :param name:
    :return:
    """
    sub_commands = {
        "list": list_sets_fc,
        "new": new_set_fc,
        "modify": modify_set_fc,
        "select": select_set_fc,
    }
    try:
        return sub_commands[c](name)
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
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
        print("Add description: (press Enter twice to stop)")
        x = input().strip()
        description = x
        while len(x):
            x = input().strip()
            description += "\n" + x

        description = description.strip()
        create_folder(FLASHCARDS_CONFIG_FOLDER_PATH + "/" + SELECTED_STUDY_SET)

        filename = spaces_to_colons(
            "".join(e for e in name if (e.isalnum() or e == " "))
        )

        with open(
            FLASHCARDS_CONFIG_FOLDER_PATH
            + "/"
            + SELECTED_STUDY_SET
            + "/"
            + filename
            + ".txt",
            "a",
        ) as fp:
            fp.write(colons_to_spaces(filename) + "\n")
            fp.write(description)
    else:
        click.echo(chalk.red("No set selected"))


def check_sub_command_cards_flashcards(c, name):
    """
    command checker flashcards cards
    :param c:
    :param name:
    :return:
    """
    sub_commands = {"add": add_card_fc}
    try:
        return sub_commands[c](name)
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
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
        click.echo(chalk.red("No set selected"))
    else:
        description = get_set_descriptions()[SELECTED_STUDY_SET]
        click.echo("Selected set: " + SELECTED_STUDY_SET)
        click.echo("Description: " + description)
        if os.path.isdir(FLASHCARDS_CONFIG_FOLDER_PATH + "/" + SELECTED_STUDY_SET):
            cards_in_selected_set = str(
                len(listdir(FLASHCARDS_CONFIG_FOLDER_PATH + "/" + SELECTED_STUDY_SET))
            )
            click.echo("No. of cards in selected set: " + cards_in_selected_set)
        else:
            click.echo("There are no cards in selected set ")


def study_fc(set, dummy):
    """
    start studying a set
    :param set:
    :param dummy:
    """

    if not SELECTED_STUDY_SET:
        click.echo(chalk.red("No set selected"))
    else:
        description = get_set_descriptions()[SELECTED_STUDY_SET]
        click.echo("Selected set: " + SELECTED_STUDY_SET)
        click.echo("Description: " + description)
        cards_in_selected_set = listdir(
            FLASHCARDS_CONFIG_FOLDER_PATH + "/" + SELECTED_STUDY_SET
        )
        len_cards_in_selected_set = len(cards_in_selected_set)
        width = get_terminal_width()
        if len_cards_in_selected_set == 0:
            click.echo(chalk.red("There are no cards in this set!"))
        else:
            click.echo(chalk.blue("Cards:"))
            click.echo(chalk.blue("_" * width))
            for i, card in enumerate(cards_in_selected_set):

                card_path = (
                    FLASHCARDS_CONFIG_FOLDER_PATH
                    + "/"
                    + SELECTED_STUDY_SET
                    + "/"
                    + card
                )
                with open(card_path) as fp:
                    name = None
                    description = ""
                    for line in fp.read().split("\n"):
                        line = line.strip()
                        if not name:
                            name = line
                        else:
                            description += line + "\n"
                description = description.strip()
                if i > 0:
                    click.echo("-" * width)
                click.echo(str(i) + ": " + name)
                click.echo("=" * width)
                click.echo(description)
                click.echo("=" * width)
                if i < len_cards_in_selected_set:
                    input("Press Enter to continue to next card")


@learn.command()
@click.pass_context
@click.argument("domain", nargs=1, required=False, callback=alias_checker)
@click.argument("action", nargs=1, required=False, callback=alias_checker)
@click.argument("name", nargs=-1, required=False, callback=alias_checker)
def flashcards(ctx, domain, action, name):
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
    domain, action, name = get_arguments(ctx, 3)
    domain = str(domain)
    action = str(action)
    name = tuple_to_string(name)
    domains = {
        "cards": check_sub_command_cards_flashcards,
        "sets": check_sub_command_sets_flashcards,
        "status": status_fc,
        "study": study_fc,
        "select": select_set_fc,
    }
    try:
        domains[domain](action, name)
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
        click.echo('Try "yoda flashcards --help" for more info')


# ----------------------- / flashcards code -----------------------#

# ----------------------- dictionary code -----------------------#
@learn.command()
@click.pass_context
@click.argument("dictionary_option", nargs=1, required=True, callback=alias_checker)
@click.argument("word", nargs=1, required=False, callback=alias_checker)
def dictionary(ctx, dictionary_option, word):
    """
        Get the definition, synonym, antonym or example of a word.
        \nOptions : define, synonym, antonym, example
    """
    dictionary_option_list = {}
    dictionary_option_list["define"] = "definitions"
    dictionary_option_list["synonym"] = "synonyms"
    dictionary_option_list["antonym"] = "antonyms"
    dictionary_option_list["example"] = "examples"

    dictionary_option = get_arguments(ctx, 1)
    word = get_arguments(ctx, 1)
    _word = str(word)

    if dictionary_option not in dictionary_option_list.keys():
        click.echo(chalk.red("Please use the right dictionary command."))
        sys.exit()

    r = requests.get(
        "https://wordsapiv1.p.mashape.com/words/"
        + _word
        + "/"
        + dictionary_option_list[dictionary_option],
        headers={
            "X-Mashape-Key": "Yq72o8odIlmshPTjxnTMN1xixyy5p1lgtd0jsn2NsJfn7pflhR",
            "Accept": "application/json",
        },
    )
    data = r.json()

    try:
        _word = data["word"]
        posted = False
        if dictionary_option == "define" and len(data["definitions"]):
            if not posted:
                click.echo(
                    chalk.blue(
                        'A few definitions of the word "'
                        + _word
                        + '" with their parts of speech are given below:'
                    )
                )
                click.echo("---------------------------------")
                posted = True

            for definition in data["definitions"]:
                print(definition["partOfSpeech"] + ": " + definition["definition"])

        elif len(data[dictionary_option_list[dictionary_option]]):
            if not posted:
                click.echo(
                    chalk.blue(
                        "A few "
                        + dictionary_option_list[dictionary_option]
                        + ' of the word "'
                        + _word
                        + '" are given below:'
                    )
                )
                click.echo("---------------------------------")
                posted = True

            for dictionary_value in data[dictionary_option_list[dictionary_option]]:
                print(dictionary_value)

        if posted and dictionary_option in ["antonym", "example"]:
            pass
        # if this word is not in the vocabulary list, add to it!
        elif posted:
            words = get_words_list()
            if _word in words:
                click.echo(
                    chalk.blue(
                        "This word already exists in the vocabulary set, so you can practice it while using that"
                    )
                )
            else:
                with open(VOCAB_LIST, "a") as fp:
                    fp.write(
                        "{} - {}\n".format(
                            _word, data[dictionary_option_list[dictionary_option]][0]
                        )
                    )
                click.echo(
                    chalk.blue(
                        "This word does not exist in the vocabulary set, so it has been added to it so that you can "
                        "practice it while using that"
                    )
                )
        else:
            click.echo(
                chalk.red(
                    "Sorry, no "
                    + dictionary_option_list[dictionary_option]
                    + " were found for this word"
                )
            )
    except KeyError:
        click.echo(chalk.red("Sorry, no definitions were found for this word"))


def get_words_list():
    words = []
    with open(VOCAB_LIST, "r") as word_list:
        for line in word_list:
            word = line.split("-")[0].strip()
            words.append(word)

    return words


# ----------------------- / dictionary code -----------------------#
