import click
import chalk
import config
import os
import apiai
import json

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get(
    'API_AI_SESSION_ID', config.API_AI_SESSION_ID)


def process(input_string):
    request.query = input_string
    response = request.getresponse().read()
    output = json.loads(response)
    answer = output["result"]["fulfillment"]["speech"]
    chalk.blue('Yoda speaks:')
    click.echo(answer)
