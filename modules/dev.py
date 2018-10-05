from __future__ import absolute_import
from __future__ import division

import json
import re
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
    """
    Find the geographical location of a given IP address.
    """
    # import pdb; pdb.set_trace()
    ip_address = get_arguments(ctx, 1)
    if not ip_address:
        return click.echo('Please supply an IP address as follows: $ yoda iplookup <ip_address>')

    _ip_address = str(ip_address)

    import geoip2.database

    path = os.path.dirname(sys.modules['yoda'].__file__)
    path = os.path.join(path, 'resources/databases/GeoLite2-City.mmdb')

    reader = geoip2.database.Reader(path)
    response = reader.city(_ip_address)
    return click.echo('{0}, {1}'.format(response.subdivisions.most_specific.name, response.country.name))


@dev.command()
@click.pass_context
@click.argument('link', nargs=1, required=True)
def checksite(ctx, link):
    """
    Check if website is up and running.
    """
    click.echo('Connecting...')

    # request
    try:
        r = requests.get(link)
    except Exception as e:
        click.echo('Looks like {0} is not a valid URL, check the URL and try again.'.format(link))
        return

    # check the status code
    if r.status_code != 200:
        click.echo("Uh-oh! Site is down. :'(")
    else:
        click.echo('Yay! The site is up and running! :)')


@dev.command()
@click.pass_context
@click.argument('astrological_sign', nargs=1, required=False, callback=alias_checker)
def horoscope(ctx, astrological_sign):
    """
    Find the today's horoscope for the given astrological sign.
    """
    astrological_sign = get_arguments(ctx, 1)
    _astrological_sign = str(astrological_sign)

    try:
        r = requests.get('http://horoscope-api.herokuapp.com/horoscope/today/{0}'.format(astrological_sign))
        return click.echo(r.json()['horoscope'])
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

# idea list process
@dev.command()
@click.argument('pattern', nargs=1)
@click.argument('path', nargs=1)
@click.option('-r', nargs=1, required=False, default=False)
@click.option('-i', nargs=1, required=False, default=False)
def grep(pattern, path, r, i):
    """
        Grep for a pattern in a file or recursively through a folder.

        yoda dev grep PATTERN PATH [OPTIONAL ARGUMENTS]
    """
    recursive, ignorecase = r, i
    if ignorecase:
        pattern = re.compile(pattern, flags=re.IGNORECASE)
    else:
        pattern = re.compile(pattern)
    if os.path.isfile(path):
        if recursive:
            click.echo(chalk.red(
                'Cannot use recursive flag with a file name.'))
            return
        with open(path, 'r') as infile:
            for match in search_file(pattern, infile):
                click.echo(match, nl=False)
    else:
        for dirpath, dirnames, filenames in os.walk(path, topdown=True):
            for filename in filenames:
                with open(os.path.join(dirpath, filename), 'r') as infile:
                    for match in search_file(pattern, infile):
                        click.echo(match, nl=False)
            if not recursive:
                break


def search_file(pattern, infile):
    for line in infile:
        match = pattern.search(line)
        if match:
            yield line


@dev.command()
@click.argument('github_login', nargs=1)
@click.argument('github_password', nargs=1)
def gitsummary(github_login, github_password):
    """
        Gets Github user stats - commits (all), repos (24hr), issues (24hr), pull requests (24hr).
        :param github_login:
        :param github_token:
    """
    from github import Github
    from datetime import datetime, timedelta
    from time import strftime

    gh = Github(github_login, github_password)
    count_repos, count_pr, count_issues, count_pr, count_commits = 0, 0, 0, 0, 0

    yesterday = datetime.today() - timedelta(days=3)
    offset_yesterday = yesterday.replace(microsecond=0).isoformat() + strftime('%z')

    # pr are considered issues by github as well
    click.echo('Fetching data. Patience you must have, my young padawan.')
    for issue in gh.search_issues('', author=github_login, state='open', created='>{}'.format(offset_yesterday)):
        if issue.pull_request:
            count_pr += 1
        else:
            count_issues += 1

    # one commit can appear in few branches
    tmp_commits = set()
    for repo in gh.get_user().get_repos():
        count_repos += 1
        for branch in repo.get_branches():
            for commit in repo.get_commits(sha=branch.name, author=github_login, since=yesterday):
                tmp_commits.add(commit.sha)
    count_commits = len(tmp_commits)

    click.echo('{}, ready your GitHub statistics are. {} repositories you have.'.format(
        github_login.capitalize(), count_repos))
    click.echo('In last 24 hours {} commit(s), {} pull requests(s) and {} issue(s) you made.'.format(
        count_commits, count_pr, count_issues
    ))
