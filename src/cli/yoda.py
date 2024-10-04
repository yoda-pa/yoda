import typer

from yodapa import hi
from yodapa.hi import add_numbers

app = typer.Typer()


@app.command()
def hello(name: str):
    """Greet someone by name."""
    typer.echo(hi.hu(name))


@app.command()
def add(a: int, b: int):
    """Add two numbers."""
    result = add_numbers(a, b)
    typer.echo(f"The sum of {a} and {b} is {result}")


if __name__ == "__main__":
    app()
