import os
import click
import json
from .config import DEFAULT_CONFIG_PATH

def _check_for_commands(keep_path):
    """Exit the program if no command have been registered."""
    if not os.path.exists(keep_path):
        click.echo("You have not registered any command yet.")
        quit()

def _show_results(results):
    """Display the results of a find."""
    if len(results) == 0:
        click.echo("Could not find any command with these parameters.")
    else:
        for kw, result in results.items():
            click.echo(kw.upper())
            for dic in result:
                if dic["explanation"] != "":
                    click.echo("\t#%i\t%s \n\t%s" %(dic["id"], dic["command"], dic["explanation"]))
                else:
                    click.echo("\t#%i\t%s" % (dic["id"], dic["command"]))

def _save_document(keep_path, keep_json):
    """Save the keep document."""
    with open(keep_path, 'w+') as keep_file:
        keep_file.write(json.dumps(keep_json))

@click.group()
@click.pass_context
def keep(ctx):
    """Keep module, for safe-keeping commands with keywords."""
    keep_path = os.path.join(DEFAULT_CONFIG_PATH, 'keep/.keep.json')
    keep_dirname = os.path.dirname(keep_path)
    ctx.ensure_object(dict)
    if not os.path.exists(keep_dirname):
        os.makedirs(keep_dirname)
    if not os.path.exists(keep_path):
        ctx.obj["keep"] = {
            "command2Id": {},
            "id2Command": {},
            "keyword2Ids": {},
            "id2Explanation": {},
            "next_id": 0
        }
    else:
        with open(keep_path, 'r') as keep_file:
            ctx.obj["keep"] = json.load(keep_file)
    ctx.obj["keep_path"] = keep_path

@keep.command()
@click.pass_context
@click.argument('command')
@click.option(
    '-k',
    '--keyword',
    multiple=True,
    help='Keyword used to retreive this command, can be invoked multiple times.',
    required=True
)
@click.argument(
    'explanation',
    nargs=-1
)
def save(ctx, command, keyword, explanation):
    """
    Save a command for later.
    Use keywords to find it when you will need it again.\n
    USAGE : yoda keep save -k find -k textfiles -k name 'find . -name "*.txt"' command used to find textfiles by name
    """
    keep = ctx.obj["keep"]
    keep_path = ctx.obj["keep_path"]
    clean_command = command.strip()
    clean_keywords = [x.encode("utf8").strip() for x in keyword]
    clean_explanation = ' '.join(x.encode("utf8").strip() for x in explanation)
    if clean_command in keep["command2Id"]:
        click.echo('%s is already registered.' % clean_command)
        return
    
    command_id = keep["next_id"]
    keep["next_id"] += 1
    keep["command2Id"][clean_command] = command_id
    keep["id2Command"][command_id] = clean_command 
    for kw in clean_keywords:
        if kw in keep["keyword2Ids"]:
            keep["keyword2Ids"][kw].append(command_id)
        else:
            keep["keyword2Ids"][kw] = [command_id]
    if explanation is not "":
        keep["id2Explanation"][command_id] = clean_explanation
    _save_document(ctx.obj["keep_path"], keep)
    click.echo("%s has been properly registered, with id #%i." % (clean_command, command_id))

@keep.command()
@click.pass_context
def findall(ctx):
    """
    Find all commands, with their keywords.
    USAGE: yoda keep findall
    """
    _check_for_commands(ctx.obj["keep_path"])
    keep = ctx.obj["keep"]
    results = {}
    for kw, command_ids in keep["keyword2Ids"].items():
        results[kw] = []
        for command_id in command_ids:
            command = keep["id2Command"][str(command_id)]
            explanation = keep["id2Explanation"][str(command_id)]
            results[kw].append({ 
                "id": command_id,
                "command": command,
                "explanation": explanation
            })
    _show_results(results)

@keep.command()
@click.pass_context
@click.option(
    '-k',
    '--keyword',
    multiple=True,
    help='Keyword used to retrive stored commands, can be invoked multiple times.',
    required=True
)
def find(ctx, keyword):
    """
    Find a command using its keywords.\n
    USAGE: yoda keep find -k keyword1 -k keyword2 -k keywordN
    """
    _check_for_commands(ctx.obj["keep_path"])
    clean_keywords = [x.encode("utf8").strip() for x in keyword]
    keep = ctx.obj["keep"]
    results = {}
    for kw in clean_keywords:
        if kw in keep["keyword2Ids"]:
            result = []
            command_ids = keep["keyword2Ids"][kw]
            for command_id in command_ids:
                result.append({ 
                    "command": keep["id2Command"][str(command_id)],
                    "explanation": keep["id2Explanation"][str(command_id)],
                    "id": command_id
                })
                results[kw] = result
    _show_results(results)

@keep.command()
@click.pass_context
@click.option(
    '-i',
    '--command-id',
    multiple=True,
    help="The command ID, (digit behind '#' when doing a find).",
    required=True
)
def remove(ctx, command_id):
    """
    Remove a command from the keep, using its #id.
    USAGE: yoda keep remove -i 1 -i 30 -i N
    """
    _check_for_commands(ctx.obj["keep_path"])
    keep = ctx.obj["keep"]
    for cid in command_id:
        for kw, command_ids in keep["keyword2Ids"].items():
            if int(cid) in command_ids:
                command_ids.remove(int(cid))
            if len(keep["keyword2Ids"][kw]) == 0:
                del keep["keyword2Ids"][kw]
        if cid in keep["id2Command"]:
            command = keep["id2Command"][cid]
            del keep["id2Command"][cid]
            del keep["command2Id"][command]
        if cid in keep["id2Explanation"]:
            del keep["id2Explanation"][cid]
        click.echo("The command #%s has been removed." % cid)
    _save_document(ctx.obj["keep_path"], keep)
