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
