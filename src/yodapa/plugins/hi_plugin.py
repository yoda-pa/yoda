from typing import Annotated, Optional

import typer

from yodapa.interfaces.plugin_interface import YodaPluginInterface


class HiPlugin(YodaPluginInterface):
    def get_app(self):
        app = typer.Typer()

        @app.command()
        def hello(name: Annotated[Optional[str], typer.Argument()] = None):
            """Say hello."""
            name = name or "Hello from Yoda!"
            typer.echo(f"Hello {name}!!!!!!!!!!!!!!!!!!!")

        return app

    def name(self) -> str:
        return "hi"
