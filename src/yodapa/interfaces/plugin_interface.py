from abc import ABC, abstractmethod

import typer


class YodaPluginInterface(ABC):
    """Interface for Yoda plugins."""

    @abstractmethod
    def name(self) -> str:
        """Name of the plugin. Also used as the subcommand name."""
        pass

    @abstractmethod
    def get_app(self) -> typer.Typer:
        """
        Return the Typer app instance for the plugin.
        This app will then be registered as a subcommand.
        """
        pass
    #
    # @abstractmethod
    # def register(self, app: typer.Typer):
    #     """Register the plugin with Yoda."""
    #     pass
    #
    # @abstractmethod
    # def configure(self):
    #     """Configure the plugin with Yoda."""
    #     pass
    #
    # @abstractmethod
    # def run(self):
    #     """Run the plugin."""
    #     pass
    #
    # @abstractmethod
    # def cleanup(self):
    #     """Clean up the plugin."""
    #     pass
