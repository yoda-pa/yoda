import click
import chalk
import setup
import github
from dulwich import porcelain
from os import mkdir

from config import get_config_file_paths
from util import *


def process(input):
    gh_username = setup.get_gh_username()
    gh_password = setup.decrypt_password()
    gh = github.Github(gh_username, gh_password)
    click.echo(chalk.blue('you are in git module'))
    click.echo('input = %s' % input)
    USER_CONFIG_FILE_PATH = get_config_file_paths()['USER_CONFIG_FILE_PATH']
    USER_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(USER_CONFIG_FILE_PATH)
    repo = porcelain.init(USER_CONFIG_FOLDER_PATH)
    porcelain.add(repo)
    porcelain.commit(repo, "A sample commit")
    porcelain.remote_add(repo, ".yoda", "https://github.com/manparvesh/.yoda")
    porcelain.push(repo, "https://github.com/manparvesh/.yoda")
