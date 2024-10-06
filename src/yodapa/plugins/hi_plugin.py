import typer

from yodapa.plugin_manager.decorator import yoda_plugin


@yoda_plugin(name="hi")
class HiPlugin:
    """
    Hi plugin. Say hello.

    Example:
        $ yoda hi hello --name MP
        $ yoda hi hello
    """

    def hello(self, name: str = None):
        """Say hello."""
        name = name or "Padawan"
        typer.echo(f"Hello {name}!")

    def _private_method_should_not_be_added(self):
        """This method should not be added as a command."""
        raise NotImplementedError()
