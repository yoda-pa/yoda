from __future__ import absolute_import
from __future__ import division

import json
import sys
from builtins import range
from builtins import str

import pyspeedtest
import requests

from past.utils import old_div

from .util import *

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

    try:
        ping = speed_test.ping()
    except requests.exceptions.ConnectionError:
        click.echo(chalk.red('Yoda cannot sense the internet right now!'))
        sys.exit(1)
    except Exception:
        click.echo(chalk.red('Speedtest servers not available'))
        sys.exit(0)

    click.echo('Speed test results:')
    click.echo('Ping: ' + '{:.2f}'.format(ping) + ' ms')

    download_speed = old_div(speed_test.download(), (1024 * 1024))
    click.echo('Download: ' + '{:.2f}'.format(download_speed) + ' Mb/s')

    upload_speed = old_div(speed_test.upload(), (1024 * 1024))
    click.echo('Upload: ' + '{:.2f}'.format(upload_speed) + ' Mb/s')


# code for URL command


def url_shorten(url_to_be_shortened):
    """
    shorten url
    :param url_to_be_shortened: 
    """
    try:
        r = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTENER_API_KEY,
                          data=json.dumps({
                              'longUrl': url_to_be_shortened
                          }), headers={
                'Content-Type': 'application/json'
            })
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    response = 'Here\'s your shortened URL:\n' + data['id']
    click.echo(response)


def url_expand(url_to_be_expanded):
    """
    expander
    :param url_to_be_expanded: 
    """
    try:
        r = requests.get(
            'https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTENER_API_KEY +
            '&shortUrl=' + url_to_be_expanded)
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    response = 'Here\'s your original URL:\n' + data['longUrl']
    click.echo(response)


def check_sub_command_url(action, url_to_be_expanded_or_shortened):
    """
    command checker for url shortener and expander
    :param action: 
    :param url_to_be_expanded_or_shortened: 
    :return: 
    """
    sub_commands = {
        'shorten': url_shorten,
        'expand': url_expand
    }
    try:
        return sub_commands[action](url_to_be_expanded_or_shortened)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda url --help" for more info')


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
    _input = str(input)
    _url = str(url)
    check_sub_command_url(_input, _url)


@dev.command()
def hackernews():
    """
    Hacker news top headlines
    """
    _url = 'https://newsapi.org/v2/everything?sources=hacker-news&apiKey=534594afc0d64a11819bb83ac1df4245'
    response = requests.get(_url)
    result = response.json()
    if result['status'] == 'ok':
        for index, item in enumerate(result['articles']):
            counter = '{}/{} \n'.format((index + 1), len(result['articles']))

            title = item['title'] or 'No title'
            description = item['description'] or 'No description'
            url = item['url'] or 'No url'

            click.echo('News-- ' + counter)
            click.echo('Title--  ' + title)
            click.echo('Description-- ' + description)
            click.echo('url-- ' + url)
            click.echo()
            click.echo('Continue? [press-"y"] ')
            c = click.getchar()
            click.echo()  # newline after news item
            if c != 'y':
                break
    else:
        click.echo('Error in api')


@dev.command()
def coinflip():
    """
    Flips a coin and displays an outcome
    """
    import random
    side = random.randint(1, 100) % 2
    click.echo('Heads' if side == 1 else 'Tails')


@dev.command()
def portscan():
    """
    Scan open ports of a website,
    utilizing multi-threading to speed the task along
    """
    import threading
    import re
    from Queue import Queue

    def scanPortsTask(port):
        import socket

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socket.connect((targetForScan, port))
            with lock_output:
                click.echo('port:' + str(port) + ' is open')

        except Exception as e:
            pass

    def taskMaster():

        while True:
            port = port_queue.get()
            scanPortsTask(port)
            port_queue.task_done()

    lock_output = threading.Lock()
    port_queue = Queue()
    targetForScan = input('Where scan ports, should I: ')
    pattern = '([\da-z\.-]+)\.([a-z\.]{2,6})$'

    if re.match(pattern, targetForScan):
        for x in range(200):
            t = threading.Thread(target=taskMaster)

            t.daemon = True
            t.start()

        for worker in range(1, 1000):
            port_queue.put(worker)

        port_queue.join()
    else:
        click.echo('Find ' + targetForScan + ' I cannot, ' + 'sure spelled correctly, are you?')