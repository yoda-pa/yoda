import typer

app = typer.Typer(help="""
    Bye plugin. Say goodbye.

    Example:

        $ yoda bye goodbye --name MP

        $ yoda bye goodbye
    """)


@app.command()
def goodbye(name: str = None):
    """Say goodbye."""
    name = name or "Padawan"
    typer.echo(f"Goodbye {name}!")
