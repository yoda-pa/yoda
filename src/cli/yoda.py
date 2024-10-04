import typer
from yodapa import hi

app = typer.Typer()

@app.command()
def hello(name: str):
    """Greet someone by name."""
    typer.echo(hi.hu(name))

if __name__ == "__main__":
    app()
