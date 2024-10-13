from typing import Annotated, Optional

import typer

from yodapa.plugin import discover_plugins, load_plugins
from yodapa.plugins.plugin import get_enabled_plugins

app = typer.Typer()
plugins = discover_plugins()

enabled_plugins = get_enabled_plugins()

load_plugins(app, [(plugin_name, typer_app) for plugin_name, typer_app in plugins if plugin_name in enabled_plugins])


@app.command()
def hello(name: Annotated[Optional[str], typer.Argument()] = None):
    """Say hello."""
    name = name or "Skywalker"
    typer.echo(f"Hello {name}!")


if __name__ == "__main__":
    app()
