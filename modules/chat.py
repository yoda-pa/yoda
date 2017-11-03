import json
import os
import socket
import sys

import apiai
import chalk
import click

import config

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get(
    'API_AI_SESSION_ID', config.API_AI_SESSION_ID)


def process(input_string):
    """
    minimal chat bot
    :param input_string:
    """
    request.query = input_string
    try:
        response = request.getresponse().read()
    except socket.gaierror:
        # if the user is not connected to internet dont give a response 
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    output = json.loads(response)
    answer = output["result"]["fulfillment"]["speech"]
    chalk.blue('Yoda speaks:')
    click.echo(answer)
