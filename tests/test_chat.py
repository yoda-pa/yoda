# coding=utf-8
from mock import patch, MagicMock
from unittest import TestCase
from click.testing import CliRunner

import yoda

HELLO_JSON_RESPONSE = (
    '{"id": "55e0f6b9-be28-4314-9b44-4b55702029fa", '
    '"timestamp": "2019-04-05T11:56:33.632Z", "lang": "en", "result": '
    '{"source": "domains","resolvedQuery": "hello ", "action":'
    '"smalltalk.greetings.hello","actionIncomplete": false, "parameters": {},'
    '"contexts": [],"metadata": {},"fulfillment": {"speech":'
    '"Good day!", "messages": [{"type": 0,  "speech": "Hey there!"}]},'
    '"score": 1.0}, "status": {"code": 200,"errorType":"success"}, '
    '"sessionId": "dd60fde7-c6ab-4f38-9487-7300c42b4916"}'
)


class TestChat(TestCase):
    """
        Test for the following commands:

        | Module: chat
        | command: chat
    """

    def __init__(self, methodName="runTest"):
        super(TestChat, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        with patch('modules.chat.request') as request:
            request.getresponse().read = MagicMock(return_value=HELLO_JSON_RESPONSE.encode('utf-8'))
            result = self.runner.invoke(yoda.cli, ["chat", "hello"])
            self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["chat"])
        self.assertEqual(result.exit_code, 0)
