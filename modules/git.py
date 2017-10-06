import click
import chalk
import setup
import github
from dulwich import porcelain

from config import get_config_file_paths
import util


def process(input):
    gh_username = setup.get_gh_username()
    gh_password = setup.decrypt_password()
    github.Github(gh_username, gh_password)
    click.echo(chalk.blue('you are in git module'))
    click.echo('input = %s' % input)
    USER_CONFIG_FILE_PATH = get_config_file_paths()['USER_CONFIG_FILE_PATH']
    USER_CONFIG_FOLDER_PATH = util.get_folder_path_from_file_path(
        USER_CONFIG_FILE_PATH)
    repo = porcelain.init(USER_CONFIG_FOLDER_PATH)
    porcelain.add(repo)
    porcelain.commit(repo, "A sample commit")
    porcelain.remote_add(repo, ".yoda", "https://github.com/manparvesh/.yoda")
    porcelain.push(repo, "https://github.com/manparvesh/.yoda")
