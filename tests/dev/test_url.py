# coding=utf-8
from builtins import str
from mock import patch, MagicMock
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestSpeedtest(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: url
    """
    URL_SHORTEN_RESPONSE = {
        u'previewLink': u'https://yodacli.page.link/w7zEiUimwB1nMqwRA?d=1',
        u'warning': [
            {u'warningCode': u'UNRECOGNIZED_PARAM',
             u'warningMessage': u"iOS app 'com.yodacli' lacks App ID Prefix.]"},
        ],
        u'shortLink': u'https://yodacli.page.link/RpXwYjkpLr5cT5Kd9'
    }
    URL_EXPAND_RESPONSE = {
        u'status': u'OK', u'kind': u'urlshortener#url',
        u'id': u'https://yodacli.page.link/RpXwYjkpLr5cT5Kd9',
        u'longUrl': u'https://yodacli.page.link/?link=http://manparvesh.com/'
    }

    def __init__(self, methodName="runTest"):
        super(TestSpeedtest, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        with patch('modules.dev.requests') as requests:
            # shorten url
            url_to_test = "http://manparvesh.com/".strip()
            requests.post().json.return_value = self.URL_SHORTEN_RESPONSE
            result = self.runner.invoke(yoda.cli, ["url", "shorten", url_to_test])
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode("ascii", "ignore").decode("utf-8"))
            self.assertEqual(type(output_string), str)
            self.assertTrue(output_string.startswith("Here's your shortened URL:"))
            shortened_url = str(output_string[str(output_string).find("http"):]).strip()

        with patch('modules.dev.requests') as requests:
            requests.get().json.return_value = self.URL_EXPAND_RESPONSE
            # expand url
            result_decode = self.runner.invoke(yoda.cli, ["url", "expand", shortened_url])
            self.assertEqual(result_decode.exit_code, 0)
            second_output_string = str(
                result_decode.output.encode("ascii", "ignore").decode("utf-8")
            )

            self.assertEqual(type(second_output_string), str)
            self.assertTrue(second_output_string.startswith("Here's your original URL:"))
            expanded_url = str(
                second_output_string[str(second_output_string).find("http"):]
            ).strip()

            # check if the original url and obtained url are equal
            self.assertEqual(url_to_test, expanded_url)

        # incorrect command should show our custom response instead of stacktrace
        result = self.runner.invoke(yoda.cli, ["url", "incorrect_subcommand", "aaa"])
        self.assertEqual(result.exit_code, 0)
        final_output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
        self.assertTrue(
            final_output_string.endswith('Try "yoda url --help" for more info')
        )
