import typer

from yodapa.plugin_manager.decorator import yoda_plugin


@yoda_plugin(name="bye")
class ByePlugin:
    """
    Bye plugin. Say goodbye.

    Example:
        $ yoda bye goodbye --name MP
        $ yoda bye goodbye
    """

    def goodbye(self, name: str = None):
        """Say goodbye."""
        name = name or "Padawan"
        typer.echo(f"Goodbye {name}!")
