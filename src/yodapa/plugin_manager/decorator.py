import inspect
from typing import Annotated, Optional

import typer


def yoda_plugin(name: Annotated[Optional[str], typer.Argument()] = None):
    """
    Decorator to turn a class into a Yoda PA plugin.
    All public methods of the class are added as Typer commands.
    """

    def decorator(cls):
        nonlocal name
        name = name or cls.__name__.lower()

        def __init__(self):
            self.typer_app = typer.Typer(name=name, help=f"{name} plugin commands")

            for method_name, method in inspect.getmembers(self, predicate=inspect.ismethod):
                # Skip private methods
                if method_name.startswith("_"):
                    continue

                self.typer_app.command()(method)

        cls.__init__ = __init__
        cls.name = name
        return cls

    return decorator
