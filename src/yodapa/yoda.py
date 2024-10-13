from typing import Annotated, Optional

import typer

from yodapa.core.config import initialize_config
from yodapa.core.util import init_plugins

app = typer.Typer()
init_plugins(app)


@app.command()
def hello(name: Annotated[Optional[str], typer.Argument()] = None):
    """Say hello."""
    name = name or "Skywalker"
    typer.echo(f"Hello {name}!")


@app.command()
def init():
    """Init yoda configurations"""
    initialize_config()


if __name__ == "__main__":
    app()
