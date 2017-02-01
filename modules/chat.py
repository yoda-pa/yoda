import click
import chalk
import config
import os
import apiai
import json
import emoji

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get('API_AI_SESSION_ID', config.API_AI_SESSION_ID)

def process(input):
    click.echo(chalk.blue('you are in chat module'))
    click.echo('input = %s' % input)
    request.query = input
    click.echo('output: ')
    response = request.getresponse().read()
    output = json.loads(response)
    answer = output["result"]["fulfillment"]["speech"]
    if output['status']['errorType'] == 'success':
        click.echo(response)
        click.echo(emoji.emojize('The dude is :fire:'))
    else:
        click.echo('some error')
