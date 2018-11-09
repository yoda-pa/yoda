import click

from .config import get_config_file_paths
from .util import get_folder_path_from_file_path, create_folder


ALIAS_CONFIG_FILE_PATH = get_config_file_paths()["ALIAS_CONFIG_FILE_PATH"]
ALIAS_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(ALIAS_CONFIG_FILE_PATH)


class Alias(click.Group):

    _aliases = {}

    def __init__(self, *args, **kwargs):
        create_folder(ALIAS_CONFIG_FOLDER_PATH)
        try:
            with open(ALIAS_CONFIG_FOLDER_PATH + "/alias.txt", "r") as f:
                lines = f.readlines()
                for i in range(1, len(lines), 2):
                    Alias._aliases[lines[i].strip("\n")] = (
                        lines[i - 1].strip("\n").split()
                    )
        except:
            fo = open(ALIAS_CONFIG_FOLDER_PATH + "/alias.txt", "w")
            fo.close()
        super(Alias, self).__init__(*args, **kwargs)

    # this implementation does not work with current version of click
    # def __call__(self, *args, **kwargs):
    #     if len(args) != 0 and args[0][0] in _aliases:
    #         alias = _aliases[args[0][0]]
    #         args[0].pop(0)
    #         for command in reversed(alias):
    #             args[0].insert(0, command)
    #     return super(Alias, self).__call__(*args, **kwargs)

    def get_command(self, ctx, cmd_name):
        ctx.obj = []
        cmd = click.Group.get_command(self, ctx, cmd_name)
        if cmd is not None:
            return cmd

        if cmd_name in Alias._aliases.keys():
            ctx.obj = Alias._aliases[cmd_name][1:]
            return click.Group.get_command(self, ctx, Alias._aliases[cmd_name][0])

        return None


def alias_checker(ctx, param, value):
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


@click.group()
def alias():
    """
        For creating aliases to cumbersome commands
    """


@alias.command()
@click.argument("orig_cmd", nargs=1)
@click.argument("alias_cmd", nargs=1)
def new(orig_cmd, alias_cmd):
    """
        Alias a new command \n\n
        Usage: yoda alias "yoda old command" "yoda new command" \n
    """
    if len(alias_cmd) == 0:
        click.echo("Aliasing failed - Invalid alias")
        return
    if len(orig_cmd) == 0:
        click.echo("Aliasing failed - Invalid command to alias")
        return
    if orig_cmd.split()[0] == "alias":
        click.echo("Aliasing failed - Cannot alias the alias command")
        return
    if len(alias_cmd.split()) > 1:
        click.echo("Aliasing failed - Alias must not contain spaces")
        return
    if alias_cmd in Alias._aliases.keys():
        click.echo(
            "Aliasing failed - Alias name already exists. Use alias delete to remove it"
        )
        return
    if orig_cmd and alias_cmd:
        create_folder(ALIAS_CONFIG_FOLDER_PATH)
        with open(ALIAS_CONFIG_FOLDER_PATH + "/alias.txt", "a") as f:
            f.write(orig_cmd + "\n" + alias_cmd + "\n")
        Alias._aliases[alias_cmd] = orig_cmd
        click.echo("Aliased %s as %s" % (orig_cmd, alias_cmd))


@alias.command()
@click.argument("alias", nargs=1)
def delete(alias):
    """
        Delete an alias \n\n
        Usage: yoda alias delete "alias_string" \n
    """
    if alias not in Alias._aliases.keys():
        click.echo("Alias delete failed - Could not find alias")
        return
    del Alias._aliases[alias]
    create_folder(ALIAS_CONFIG_FOLDER_PATH)
    with open(ALIAS_CONFIG_FOLDER_PATH + "/alias.txt", "w") as f:
        for key in Alias._aliases.keys():
            f.write(" ".join(Alias._aliases[key]) + "\n" + key + "\n")


@alias.command()
def show():
    """
        Delete an alias \n\n
        Usage: yoda alias delete "alias_string" \n
    """
    click.echo("alias_command : original_command")
    for key in Alias._aliases.keys():
        click.echo(key + " : " + " ".join(Alias._aliases[key]))
