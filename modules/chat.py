from __future__ import absolute_import

import json
import os
import socket
import sys
import urllib

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request

import chalk
import click

from . import config

CLIENT_ACCESS_TOKEN = os.environ.get("API_AI_TOKEN", config.API_AI_TOKEN)


QUOTE_API_URL = "https://api.forismatic.com/api/1.0/"

# required to be compatible with mocking tests
request = None

'''
setup function for apiai import and related variables
Putting these in a function improves load time for all yoda commands
'''
def import_apiai():
    global apiai, request
    import apiai

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.session_id = os.environ.get("API_AI_SESSION_ID", config.API_AI_SESSION_ID)

def process(input_string):
    import_apiai()
    """
    minimal chat bot
    :param input_string:
    """
    if "inspire" in input_string:
        send_data = {"method": "getQuote", "format": "json", "lang": "en", "key": ""}
        hdr = {"User-Agent": "Magic Browser"}
        full_url = QUOTE_API_URL + "?" + urllib.parse.urlencode(send_data)
        response = urlopen(Request(full_url, headers=hdr))
        response = response.read()
        output = json.loads(response)
        quote = output["quoteText"]
        author = output["quoteAuthor"]
        click.echo(quote)
        click.echo("- " + author)
    else:
        request.query = input_string
        try:
            response = request.getresponse().read()
        except socket.gaierror:
            # if the user is not connected to internet don't give a response
            click.echo(chalk.red("Yoda cannot sense the internet right now!"))
            sys.exit(1)

        output = json.loads(response.decode("utf-8"))
        answer = output["result"]["fulfillment"]["speech"]
        click.echo(chalk.blue("Yoda speaks:"))
        click.echo(answer)
