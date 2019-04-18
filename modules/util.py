from __future__ import print_function
from builtins import input
import errno
import os.path
import subprocess

import re

import chalk
import click
import yaml

try:
    raw_input  # Python 2
except NameError:
    raw_input = input  # Python 3


def alias_checker(ctx, param, value):
    from .alias import Alias

    if value is None or len(value) == 0:
        pass
    elif value in Alias._aliases.keys():
        ctx.obj.extend(Alias._aliases[value])
    elif type(value) == tuple:
        for val in value:
            if val in Alias._aliases.keys():
                ctx.obj.extend(Alias._aliases[val])
            else:
                ctx.obj.append(val)
    else:
        ctx.obj.append(value)
    return None


def get_arguments(ctx, n):
    if n == -1:
        args = ctx.obj[:]
        del ctx.obj[:]
        return args
    elif len(ctx.obj) >= n:
        args = ctx.obj[:n]
        del ctx.obj[:n]
        if n == 1:
            return args[0]
        return args
    else:
        args = ctx.obj[:]
        for i in range(n - len(ctx.obj)):
            args.append(None)
        del ctx.obj[:]
        if n == 1:
            return args[0]
        return args


def create_folder(folder_path):
    """
    if folder does not exist, create it
    :param folder_path:
    """
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def ask_overwrite(file_path):
    """
    asks if you want to overwrite the given file, if it exists
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        click.echo(
            chalk.red(
                "A configuration file already exists. Are you sure you want to overwrite it? (y/n)"
            )
        )
        overwrite_response = input().lower()
        if not (overwrite_response == "y" or overwrite_response == "yes"):
            return True
        return False
    return False


def input_data(data, file_path):
    """
    inputs dict into a .yaml file
    :param data:
    :param file_path:
    """
    with open(file_path, "a") as config_file:
        yaml.dump(data, config_file, default_flow_style=False)


def get_folder_path_from_file_path(file_path):
    """
    get folder path from file path
    :param file_path:
    :return:
    """
    return os.path.dirname(file_path)


def tuple_to_string(input):
    """
    convert tuple to string
    :param input:
    :return:
    """
    if input:
        test_string = ""
        for i in input:
            test_string += i + " "
        return test_string.lower().strip()


def spaces_to_colons(s):
    """
    replaces spaces in text with colons
    :param s:
    :return:
    """
    return "-".join(s.split(" "))


def colons_to_spaces(s):
    """
    replaces colons in text with spaces
    :param s:
    :return:
    """
    return " ".join(s.split("-"))


command = ["tput", "cols"]


def get_terminal_width():
    """
    get terminal width
    :return:
    """
    try:
        width = int(subprocess.check_output(command))
    except OSError as e:
        print("Invalid Command '{0}': exit status ({1})".format(command[0], e.errno))
    except subprocess.CalledProcessError as e:
        print(
            "Command '{0}' returned non-zero exit status: ({1})".format(
                command, e.returncode
            )
        )
    else:
        return width


def get_input():
    """
    gets input from the user
    :return:
    """
    return input().strip()


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents["entries"].append(data)

        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)


def clean_soup_data(data):
    data = str(data)
    cleaner = re.compile("<.*?>")
    data = re.sub(cleaner, "", data)
    return data.replace(":", "").strip()
