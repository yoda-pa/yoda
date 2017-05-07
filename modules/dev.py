import click
import chalk
import pyspeedtest
import requests
import json
from util import *

GOOGLE_URL_SHORTENER_API_KEY = "AIzaSyCBAXe-kId9UwvOQ7M2cLYR7hyCpvfdr7w"


@click.group()
def dev():
    """
        Dev command group:\n
        contains commands helpful for developers
    """


@dev.command()
def speedtest():
    """
    Run a speed test for your internet connection
    """
    speed_test = pyspeedtest.SpeedTest()

    click.echo('Speed test results:')

    ping = speed_test.ping()
    click.echo('Ping: ' + '{:.2f}'.format(ping) + ' ms')

    download_speed = speed_test.download() / (1024 * 1024)
    click.echo('Download: ' + '{:.2f}'.format(download_speed) + ' MB/s')

    upload_speed = speed_test.upload() / (1024 * 1024)
    click.echo('Upload: ' + '{:.2f}'.format(upload_speed) + ' MB/s')

# code for URL command
# shorten


def url_shorten(url):
    r = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTENER_API_KEY, data=json.dumps({
        'longUrl': url
    }), headers={
        'Content-Type': 'application/json'
    })
    data = r.json()
    response = 'Here\'s your shortened URL:\n' + data['id']
    click.echo(response)

# expander


def url_expand(url):
    r = requests.get('https://www.googleapis.com/urlshortener/v1/url', params={
        'key': GOOGLE_URL_SHORTENER_API_KEY,
        'shortUrl': url
    })
    data = r.json()
    response = 'Here\'s your original URL:\n' + data['longUrl']
    click.echo(response)

# command checker for url shortener and expander


def check_sub_command_url(action, url):
    sub_commands = {
        'shorten': url_shorten,
        'expand': url_expand
    }
    try:
        return sub_commands[action](url)
    except KeyError:
        chalk.red('Command does not exist!')
        click.echo('Try "dude url --help" for more info')


@dev.command()
@click.argument('input', nargs=1)
@click.argument('url', nargs=1)
def url(input, url):
    """
        URL shortener and expander\n\n

        Commands:
        shorten: to shorten the given URL
        expand: to expand shortened URL
    """
    input = str(input)
    url = str(url)
    check_sub_command_url(input, url)
