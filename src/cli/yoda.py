from typing import Annotated, Optional

import typer

from yodapa.config import ConfigManager
from yodapa.plugin_manager.plugin import PluginManager


class Yoda:
    """Yoda main class."""

    def __init__(self):
        self.app = typer.Typer()
        self.config = ConfigManager()
        self.plugin_manager = PluginManager(self.app, self.config)

    def init(self):
        self.plugin_manager.discover_plugins()
        self.plugin_manager.load_plugins()


yoda = Yoda()
yoda.init()

# define commands
app = yoda.app


@app.command()
def hello(name: Annotated[Optional[str], typer.Argument()] = None):
    """Say hello."""
    name = name or yoda.config.get("user", "Skywalker")
    typer.echo(f"Hello {name}!")


@app.command()
def configure():
    """Configure Yoda."""
    yoda.config.set("user", typer.prompt("What is your name?"))
    typer.echo("Yoda configured!")


if __name__ == "__main__":
    app()
