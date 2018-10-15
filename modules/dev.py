from __future__ import absolute_import
from __future__ import division

import json
import re
import sys

from builtins import range
from builtins import str

from pydub import AudioSegment
from pydub.playback import play

import pyspeedtest
import os
import requests

from past.utils import old_div

from .util import *
from .alias import alias_checker

from resources.hackerearth.language import supported_languages
from resources.hackerearth.parameters import RunAPIParameters

from resources.hackerearth.api_handlers import HackerEarthAPI

FIREBASE_DYNAMIC_LINK_API_KEY = "AIzaSyAuVJ0zfUmacDG5Vie4Jl7_ercv6gSwebc"
GOOGLE_URL_SHORTENER_API_KEY = "AIzaSyCBAXe-kId9UwvOQ7M2cLYR7hyCpvfdr7w"
domain = "yodacli.page.link"
HACKEREARTH_API_KEY = '0a7f0101e5cc06e4417a3addeb76164680ac83a4'

whois_base_url = "https://www.whois.com/whois/"


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
        r = requests.post(
            'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=' + FIREBASE_DYNAMIC_LINK_API_KEY,
            data=json.dumps({"dynamicLinkInfo": {"dynamicLinkDomain": domain, "link": url_to_be_shortened}}), headers={
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
        # res = res[:-3]
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


def add_keybindings(keybinding_filepath):
    pass


def search_keybindings(keybinding_filepath, search_editor, search_key):
    pass


def check_sub_command_keybindings(action, keybinding_filepath=None, search_editor=None, search_key=None):
    """
    command checker for keybindings
    :param action:
    :param keybinding_filepath:, 
    :param search_key : Default None,
    :return:
    """
    sub_commands = {
        'add': add_keybindings,
        'search': search_keybindings
    }
    try:
        return sub_commands[action](keybinding_filepath, search_key)
        if action == 'add':
            sub_commands[action](keybinding_filepath)
        elif action == 'search':
            sub_commands[action](search_editor,search_key)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda dev keybindings --help" for more info')


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


@dev.command()
@click.pass_context
@click.argument('path', nargs=1, required=True)
@click.argument('start', nargs=1, required=False, default=0)
@click.argument('end', nargs=1, required=False, default=0)
def mp3cutter(ctx, path, start, end):
    """
    This command can be used to cut audio tracks right inside your terminal.

    yoda dev mp3cutter MUSIC_PATH START[default: 0] END[default:lenght of music]
    """
    click.echo("\nOpening file...")

    try:
        song = AudioSegment.from_mp3(path)
    except FileNotFoundError:
        click.echo("No such file as " + path + ", plase re-check the PATH and try again :)")
        return
    except IndexError:
        click.echo("Wrong file format :'( ")
        return

    song_length = len(song)

    # Check if end point is given or not
    if not end:
        end = song_length / 1000

    # Check if end point is greater than length of song
    if end > song_length:
        click.echo("Duh! Given endpoint is greater than lenght of music :'( ")
        return

    start = start * 1000
    end = end * 1000

    if start > end:
        click.echo(
            "Given startpoint ({0}s) is greater than endpoint ({1}s) :/ ".format(start / 1000 / 60, end / 1000 / 60))
        return

    if start > song_length:
        click.echo("Given startpoint ({0}s) is greater than the lenght of music ({1}s)".format(start / 1000 / 60,
                                                                                               song_length / 1000 / 60))
        return

    click.echo("Cropping mp3 file from: " + str(start) + " to: " + str(end / 1000))

    cropped_file_location = path.replace(".mp3", "_cropped.mp3");
    # cut the mp3 file
    song = song[start:end]

    # save
    song.export(cropped_file_location, format="mp3")
    click.echo("Yay!! Successfully cropped! :)\n")

    if click.confirm("Do you want to play the cropped mp3 file?"):
        play(song)


@dev.command()
@click.pass_context
@click.argument('domain', nargs=1, required=True)
def whois(ctx, domain):
    """
    Get the information about domains.
    """

    click.echo("Verifying domain...\n")

    data_obj = get_whois_data(domain)[0]

    if not "Domain" in data_obj:
        click.echo("This domain has not been registered yet :/")
        return

    # Data that we display
    labels = ["Domain", "Registrar", "Organization", "Country", "Registered On", "Expires On", "Updated On"]

    for idx, label in enumerate(labels):
        # Eg:      "Domain:        Facebook.com"
        # Formula: Label + whitespace + value
        text_to_print = label + ":" + " " * (14 - len(label)) + data_obj[label]

        if idx == 3:
            text_to_print += "\n"
        click.echo(text_to_print)


def get_whois_data(domain):
    req = requests.get(whois_base_url + domain)
    html = req.text

    soup = BeautifulSoup(html, 'lxml')

    labels = soup.findAll('div', attrs={'class': 'df-label'})
    values = soup.findAll('div', attrs={'class': 'df-value'})

    data_obj = {}

    # convert into pythons dictionaire
    for i in range(len(labels)):
        data_obj[clean_soup_data(labels[i])] = clean_soup_data(values[i])

    return data_obj, req.status_code


@dev.command()
@click.pass_context
@click.argument('path', nargs=1, required=True)
def fileshare(ctx, path):
    '''
    Upload and share files using https://file.io.
    '''
    if os.path.isfile(path):
        response = subprocess.check_output([
            'curl',
            '-F',
            'file=@' + path,
            'https://file.io'])

        response_json = json.loads(response)
        if 'link' in response_json.keys():
            click.echo(chalk.green("File Link : " + response_json['link']))
            click.echo(chalk.yellow("WARNING: File will be deleted after it is accessed once."))
        else:
            click.echo(chalk.red("File upload failed!"))
    else:
        click.echo(chalk.red("No file such as " + path + ", Please re-check the PATH and try again."))

@dev.command()
@click.pass_context
@click.argument('input', nargs=1, required=False)
@click.argument('keybinding_filepath', nargs=1, required=False, default=None)
@click.argument('search_editor', nargs=1, required=False, default=None)
@click.argument('search_key', nargs=1, required=False, default=None)
def keybindings(ctx, path, start, end):
    """
    This command can be used to save keybinding files for different editors.

    yoda dev keybindings INPUT KEYBINDING_FILE EDITOR_TO_SEARCH[default: None] WORD_TO_SEARCH[default:None]
    """
    input, key_binding_filepath, search_editor, search_key = get_arguments(ctx, 4)
    _input = str(input)
    _key_binding_filepath = str(url)
    _search_editor = str(search_editor)
    _search_key = str(search_key)
    check_sub_command_keybindings(_input, _key_binding_filepath, _search_editor, _search_key)


def search_file(pattern, infile):
    for line in infile:
        match = pattern.search(line)
        if match:
            yield line


@dev.command()
@click.pass_context
@click.argument('path', nargs=1, required=True)
def run(ctx, path):
    """
        Compile and run code without a local compiler.
    """
    if os.path.isfile(path):
        source = open(path, 'r').read()
        file_extension = path.rsplit('.', 1)[1]

        if file_extension not in supported_languages.keys():
            click.echo(chalk.red('Sorry, Unsupported language.'))
            sys.exit(1)

        lang = supported_languages[file_extension]
        compressed = 1
        html = 0
        params = RunAPIParameters(
            client_secret=HACKEREARTH_API_KEY, source=source,
            lang=lang, compressed=compressed, html=html)

        api = HackerEarthAPI(params)

        click.echo(chalk.yellow('Compiling code..'))
        r = api.compile()

        click.echo(chalk.cyan('Running code...'))
        r = api.run()
        output = r.__dict__.get('output')

        click.echo(chalk.green('Output:'))
        click.echo(output)
        click.echo("Link: " + r.__dict__.get('web_link'))

    else:
        click.echo(chalk.red("No file such as " + path + ", Please re-check the file path and try again."))
        sys.exit(1)
