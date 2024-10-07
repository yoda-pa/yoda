# Yoda PA

[![Github CI](https://github.com/yoda-pa/yoda/actions/workflows/ci.yml/badge.svg)](https://github.com/yoda-pa/yoda/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/yodapa.svg)](https://badge.fury.io/py/yodapa)

Personal Assistant on the command line.

![Yoda](docs/docs/logo.png)

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
