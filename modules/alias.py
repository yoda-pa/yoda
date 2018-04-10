import click
import dev
from .config import get_config_file_paths
from .util import *


ALIAS_CONFIG_FILE_PATH = get_config_file_paths()["ALIAS_CONFIG_FILE_PATH"]
ALIAS_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(ALIAS_CONFIG_FILE_PATH)

class Alias(click.Group):

    def invoke(self, ctx):
        self.ctx_args = ctx.args
        super(Alias, self).invoke(ctx)

    def get_command(self, ctx, cmd_name):
        try:
            self.ctx_args
        except:
            return None

        ctx.obj = self.ctx_args

        cmd = click.Group.get_command(self, ctx, cmd_name)
        if cmd is not None:
            return cmd

        with open(ALIAS_CONFIG_FOLDER_PATH + '/alias.txt', 'r') as f:
            index = 0
            prev_cmd = None
            for line in f:
                line = line.strip('\n')

                # found the command
                if index % 2 == 1 and line == cmd_name:
                    orig_cmd = prev_cmd.split()

                    # insert extra commands
                    ctx.obj[0:0] = orig_cmd[1:]
                    return click.Group.get_command(self, ctx, orig_cmd[0])

                prev_cmd = line
                index += 1
        return None


@click.group()
def alias():
    """
        For creating aliases to cumbersome commands
    """

@alias.command()
@click.argument('old_command', nargs=1)
@click.argument('new_command', nargs=1)
def new(old_command, new_command):
    """
        Alias a new command \n\n
        Usage: yoda alias "yoda old command" "yoda new command" \n
    """
    if len(new_command) == 0:
        click.echo("Aliasing failed - Invalid alias")
        return
    if len(old_command) == 0:
        click.echo("Aliasing failed - Invalid command to alias")
        return
    if old_command.split()[0] == "alias":
        click.echo("Aliasing failed - Cannot alias the alias command")
        return
    if len(new_command.split()) > 1:
        click.echo("Aliasing failed - Alias must not contain spaces")
        return
    with open(ALIAS_CONFIG_FOLDER_PATH + '/alias.txt', 'r') as f:
        index = 0
        for line in f:
            line = line.strip()
            if index % 2 == 1 and line == new_command:
                click.echo("Aliasing failed - Alias name already exists. Use alias delete to remove it")
                return
            index += 1
    if old_command and new_command:
        create_folder(ALIAS_CONFIG_FOLDER_PATH)
        with open(ALIAS_CONFIG_FOLDER_PATH + '/alias.txt', 'a') as f:
            f.write(old_command + '\n' + new_command + '\n')

@alias.command()
@click.argument('command_alias', nargs=1)
def delete(command_alias):
    """
        Delete an alias \n\n
        Usage: yoda alias delete "alias_string" \n
    """
    f = open(ALIAS_CONFIG_FOLDER_PATH + '/alias.txt', 'r')
    lines = f.readlines()
    f.close()
    create_folder(ALIAS_CONFIG_FOLDER_PATH)
    for i in range(1, len(lines), 2):
        line = lines[i].strip()
        if line == command_alias:
            lines.pop(i - 1)
            lines.pop(i - 1)
            break
        if i + 2 >= len(lines):
            click.echo("Alias delete failed - Could not find alias")
            return
    with open(ALIAS_CONFIG_FOLDER_PATH + '/alias.txt', 'w') as f:
        for line in lines:
            f.write(line)
