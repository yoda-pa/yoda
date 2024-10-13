import os

import typer

app = typer.Typer()


@app.command()
def speedtest():
    os.system("speedtest-cli")
