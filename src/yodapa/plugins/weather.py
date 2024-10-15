import requests
import click
import typer

app = typer.Typer()

@app.command()
def get_weather(location):
    location_id = location.strip().replace(" ", "+")

    weather_service = "http://wttr.in/"

    response = requests.get(weather_service + location)
    click.echo(response.text)
