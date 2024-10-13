from typing import Annotated, Optional

import typer

from yodapa.core.plugin import init_plugins

app = typer.Typer()
init_plugins(app)


@app.command()
def hello(name: Annotated[Optional[str], typer.Argument()] = None):
    """Say hello."""
    name = name or "Skywalker"
    typer.echo(f"Hello {name}!")


if __name__ == "__main__":
    app()
