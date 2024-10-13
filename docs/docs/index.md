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

![img.png](img.png)

You can find the details for each plugin with the `--help` flag. Some examples:

![img_1.png](img_1.png)

![img_2.png](img_2.png)

![img_3.png](img_3.png)

### Write your own plugin for Yoda

Simply create a class with the `@yoda_plugin(name="plugin-name")` decorator and add methods to it. The non-private
methods will be automatically added as sub-commands to Yoda, with the command being the name you provide to the
decorator.

```python
import typer

app = typer.Typer(help="""
    Hi plugin. Say hello.

    Example:

        $ yoda hi hello --name MP

        $ yoda hi hello
    """)


@app.command()
def hello(name: str = None):
    """Say hello."""
    name = name or "Padawan"
    typer.echo(f"Hello {name}!")
```

### Use AI to generate your own plugin

```bash
$ yoda ai generate-command todo "todo list that keeps track of your todos"

🤖 Generated code:

import typer
from weather import Weather

app = typer.Typer(help="Show weather for a given location")

@app.command()
def weather(location: str):
    """Show weather for a given location."""
    try:
        weather_data = Weather(location).get_weather()
        print(f"Weather for {location}:")
        print(f"Temperature: {weather_data['temperature']}")
        print(f"Description: {weather_data['description']}")
    except KeyError as error:
        print("Invalid location")

This code uses the `Weather` class from the `weather` library to retrieve weather data for a given location. The
`location` argument is passed as a command-line argument, and the `get_weather()` method of the `Weather` object returns
a dictionary containing the current temperature and description of the weather in the given location.

The code uses a try-except block to catch any errors that may occur when retrieving the weather data, such as invalid
locations. In this case, it prints an error message to the console indicating that the location is invalid.

```

.. or chat with Yoda:
![img_5.png](img_5.png)

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
