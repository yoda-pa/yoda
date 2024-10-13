from typing import Annotated, Optional

import typer

from yodapa.plugin import discover_plugins, load_plugins

app = typer.Typer()
plugins = discover_plugins()
load_plugins(app, plugins)


@app.command()
def hello(name: Annotated[Optional[str], typer.Argument()] = None):
    """Say hello."""
    name = name or "Skywalker"
    typer.echo(f"Hello {name}!")


if __name__ == "__main__":
    app()
