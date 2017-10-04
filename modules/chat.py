import click
import chalk
import config
import os
import apiai
import json
import emoji
import unirest

CLIENT_ACCESS_TOKEN = os.environ.get('API_AI_TOKEN', config.API_AI_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = os.environ.get(
    'API_AI_SESSION_ID', config.API_AI_SESSION_ID)


def process(input):
    request.query = input

    click.echo('Getting response...')

    # -Get response of input from ApiAI
    response = request.getresponse().read()
    output = json.loads(response)
    # --error handling for ApiAI request
    if output['status']['errorType'] != 'success':
        click.echo(click.style('An error occurred requesting response from ApiAI', bg = 'white', fg = 'red'))
        return

    # -Convert response to yoda-speak
    answer = output["result"]["fulfillment"]["speech"]
    response = unirest.get("https://yoda.p.mashape.com/yoda?sentence=" + answer,
        headers={
            "X-Mashape-Key": "Yq72o8odIlmshPTjxnTMN1xixyy5p1lgtd0jsn2NsJfn7pflhR",
            "Accept": "text/plain"
        }
    )
    # --error handling for heroku request
    if response.code == 503:
        click.echo(click.style('An error occurred requesting response from speech conversion', bg = 'white', fg = 'red'))
        return

    # -Print out final reponse
    click.echo(click.style('Yoda says: {}'.format(response.body), fg = 'green'))
