from __future__ import print_function

import requests
import click
import json

from .util import *


@click.group()
def entertainment():
    """
        The entertainment module
    """


# ----------------------- lyrics code -----------------------#
@entertainment.command()
def lyrics():
    "Get the lyrics for the given artist and title."

    click.echo(chalk.blue("Enter the artist name:"))
    artist = input()
    click.echo(chalk.blue("Enter the title name:"))
    title = input()

    lyrics_request = requests.get("https://api.lyrics.ovh/v1/" + artist + "/" + title)
    lyrics_data = lyrics_request.json()

    if "lyrics" in lyrics_data.keys():
        click.echo(chalk.green("--------Lyrics--------"))
        click.echo(lyrics_data["lyrics"])
    elif "error" in lyrics_data.keys():
        click.echo(chalk.yellow(lyrics_data["error"]))
    else:  # if there is no lyrics or error in API response.
        click.echo(
            chalk.red("Something wrong with the request. Please raise an issue.")
        )


# ----------------------- / lyrics code -----------------------#
