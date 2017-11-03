import os.path
import subprocess

import chalk
import yaml


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
        chalk.red(
            'A configuration file already exists. Are you sure you want to overwrite it? (y/n)')
        overwrite_response = raw_input().lower()
        if not (overwrite_response == 'y' or overwrite_response == 'yes'):
            return True
        return False
    return False


def input_data(data, file_path):
    """
    inputs dict into a .yaml file
    :param data:
    :param file_path:
    """
    with open(file_path, 'a') as config_file:
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
        test_string = ''
        for i in input:
            test_string += (i + ' ')
        return test_string.lower().strip()


def spaces_to_colons(s):
    """
    replaces spaces in text with colons
    :param s:
    :return:
    """
    return '-'.join(s.split(' '))


def colons_to_spaces(s):
    """
    replaces colons in text with spaces
    :param s:
    :return:
    """
    return ' '.join(s.split('-'))


command = ['tput', 'cols']


def get_terminal_width():
    """
    get terminal width
    :return:
    """
    try:
        width = int(subprocess.check_output(command))
    except OSError as e:
        print("Invalid Command '{0}': exit status ({1})".format(
            command[0], e.errno))
    except subprocess.CalledProcessError as e:
        print("Command '{0}' returned non-zero exit status: ({1})".format(
            command, e.returncode))
    else:
        return width


def get_input():
    """
    gets input from the user
    :return:
    """
    return raw_input().strip()


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents['entries'].append(
            data
        )

        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)
