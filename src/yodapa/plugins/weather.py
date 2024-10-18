import requests
import click
import typer

app = typer.Typer(help="""
    weather plugin. Get the weather for a location.

    Example:

        $ yoda weather get_weather "New York" 
        
        // New York is an example, replace with desired location

    """)

@app.command(name="get")
def get_weather(location):
    location_id = location.strip().replace(" ", "+")

    weather_service = "http://wttr.in/"

    response = requests.get(weather_service + location)
    click.echo(response.text)
