import os

import typer
from rich import print

app = typer.Typer()


@app.command()
def speedtest():
    os.system("speedtest-cli")


@app.command()
def coinflip():
    import random
    value = random.randint(0, 1)
    if value == 1:
        print("[green]Heads![/]")
    else:
        print("[magenta]Tails![/]")
