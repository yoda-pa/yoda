from __future__ import absolute_import
from __future__ import division

import json
import sys

from builtins import range
from builtins import str

import pyspeedtest
import os
import requests

from past.utils import old_div

from .util import *
from .alias import alias_checker

FIREBASE_DYNAMIC_LINK_API_KEY = "AIzaSyAuVJ0zfUmacDG5Vie4Jl7_ercv6gSwebc"
GOOGLE_URL_SHORTENER_API_KEY = "AIzaSyCBAXe-kId9UwvOQ7M2cLYR7hyCpvfdr7w"
domain = "yodacli.page.link"

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
    os.system("speedtest-cli")



# code for URL command


def url_shorten(url_to_be_shortened):
    """
    shorten url
    :param url_to_be_shortened:
    """
    try:
        r = requests.post('https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=' + FIREBASE_DYNAMIC_LINK_API_KEY,
                          data=json.dumps({"dynamicLinkInfo": {"dynamicLinkDomain": domain,"link": url_to_be_shortened }}), headers={
                'Content-Type': 'application/json'
            })
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    response = 'Here\'s your shortened URL:\n' + data['shortLink']
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
    res = data['longUrl']
    if domain in data['longUrl']:
        res = data['longUrl'].split('=')[1]
        #res = res[:-3]
    response = 'Here\'s your original URL:\n' + res
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
@click.pass_context
@click.argument('input', nargs=1, required=False, callback=alias_checker)
@click.argument('url', nargs=1, required=False, callback=alias_checker)
def url(ctx, input, url):
    """
        URL shortener and expander\n\n
        Commands:
        shorten: to shorten the given URL
        expand: to expand shortened URL
    """
    input, url = get_arguments(ctx, 2)
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
    is_py2 = sys.version[0] == '2'
    if is_py2:
        import Queue as queue
    else:
        import queue as queue

    def scanPortsTask(port):
        import socket

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.settimeout(1.0)
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
    port_queue = queue.Queue()
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


@dev.command()
@click.pass_context
@click.argument('ip_address', nargs=1, required=False, callback=alias_checker)
def iplookup(ctx, ip_address):
    ip_address = get_arguments(ctx, 1)
    _ip_address = str(ip_address)

    import geoip2.database

    path = os.path.dirname(sys.modules['yoda'].__file__)
    path = os.path.join(path, 'resources/databases/GeoLite2-City.mmdb')

    reader = geoip2.database.Reader(path)
    response = reader.city(_ip_address)
    return click.echo('{0}, {1}'.format(response.subdivisions.most_specific.name, response.country.name))

def check_site_up(url):
    try:
        up = requests.head(url).status_code
        return up
    except:
        return False
