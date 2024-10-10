# Yoda PA

[![Github CI](https://github.com/yoda-pa/yoda/actions/workflows/ci.yml/badge.svg)](https://github.com/yoda-pa/yoda/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/yodapa.svg)](https://badge.fury.io/py/yodapa)

Personal Assistant on the command line.

![Yoda](logo.png)

## Installation

```bash
pip install yodapa

yoda --help
```

## Configure Yoda

```bash
yoda configure
```

## Plugins

Yoda is designed to be extensible. You can write your own plugins or use the AI to generate one for you.

### List plugins

The help command will list all the available plugins.

```bash
$ yoda --help
```

### Write your own plugin for Yoda

Simply create a class with the `@yoda_plugin(name="plugin-name")` decorator and add methods to it. The non-private
methods will be automatically added as sub-commands to Yoda, with the command being the name you provide to the
decorator.

```python
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
```

### Use AI to generate your own plugin

```bash
$ yoda ai generate-command todo "todo list that keeps track of your todos"

🤖 Generated code:

import typer

from yodapa.plugin_manager.decorator import yoda_plugin


@yoda_plugin(name="todo")
class TodoPlugin:
    """
    Todo plugin. Keeps track of your todos.

    Example:
        $ yoda todo list --all
        $ yoda todo add "Finish assignment"
        $ yoda todo done 1
        $ yoda todo delete 2
    """

    def list(self, all: bool = False):
        """List all todos."""
        if all:
            typer.echo("All todos:")
            for todo in self.todos:
                typer.echo(f"- {todo}")
        else:
            typer.echo("Active todos:")
            for todo in self.active_todos:
                typer.echo(f"- {todo}")

    def add(self, name: str):
        """Add a new todo."""
        if name == "":
            raise ValueError("Todo name cannot be empty")
        self.todos.append(name)
        typer.echo(f"Added todo '{name}'")

    def done(self, id: int):
        """Mark a todo as done."""
        if id < 0 or id >= len(self.todos):
            raise ValueError("Todo ID out of range")
        self.active_todos.remove(self.todos[id])
        typer.echo(f"Marked todo {id} as done")

    def delete(self, id: int):
        """Delete a todo."""
        if id < 0 or id >= len(self.todos):
            raise ValueError("Todo ID out of range")
        self.todos.remove(self.todos[id])
        typer.echo(f"Deleted todo {id}")

    def __init__(self):
        self.todos = []
        self.active_todos = []

if __name__ == "__main__":
    typer.run(TodoPlugin())

```

## Development setup

```bash
# 1. Install poetry from their website: https://python-poetry.org/docs/#installation

# 2. Install dependencies and this package
poetry install

# 3. Activate the virtual environment
poetry shell

# Now you should be able to communicate with yoda
yoda --help
```

### Testing

```bash
# Run tests when in the virtual environment
pytest
```
