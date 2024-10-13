import typer

from yodapa.core.config import initialize_config
from yodapa.core.util import init_plugins

app = typer.Typer()
init_plugins(app)


@app.command()
def init():
    """Init yoda configurations"""
    initialize_config()


if __name__ == "__main__":
    app()
