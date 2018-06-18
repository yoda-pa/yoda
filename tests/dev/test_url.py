# coding=utf-8
from builtins import str
from unittest import TestCase
from click.testing import CliRunner

import tempfile
import os

import yoda
from modules import config


class TestSpeedtest(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: url
    """

    def __init__(self, methodName='runTest'):
        super(TestSpeedtest, self).__init__()
        self.runner = CliRunner()

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='yoda_')
        self.original_config_path = config.get_config_folder()
        config.update_config_path(self.tempdir)

    def tearDown(self):
        # Change yoda configuration directory back
        config.update_config_path(self.original_config_path)

        # Delete the temporary directory
        for root, dirs, files in os.walk(self.tempdir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.tempdir)

    def runTest(self):
        # shorten url
        url_to_test = 'http://manparvesh.com/'.strip()
        result = self.runner.invoke(yoda.cli, ['url', 'shorten', url_to_test])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8'))

        self.assertEqual(type(output_string), str)
        self.assertTrue(output_string.startswith('Here\'s your shortened URL:'))
        shortened_url = str(output_string[str(output_string).find('http'):]).strip()

        # expand url
        result_decode = self.runner.invoke(yoda.cli, ['url', 'expand', shortened_url])
        self.assertEqual(result_decode.exit_code, 0)
        second_output_string = str(result_decode.output.encode('ascii', 'ignore').decode('utf-8'))

        self.assertEqual(type(second_output_string), str)
        self.assertTrue(second_output_string.startswith('Here\'s your original URL:'))
        expanded_url = str(second_output_string[str(second_output_string).find('http'):]).strip()

        # check if the original url and obtained url are equal
        self.assertEqual(url_to_test, expanded_url)

        # incorrect command should show our custom response instead of stacktrace
        result = self.runner.invoke(yoda.cli, ['url', 'incorrect_subcommand', 'aaa'])
        self.assertEqual(result.exit_code, 0)
        final_output_string = str(result.output.encode('ascii', 'ignore').decode('utf-8')).strip()
        self.assertTrue(final_output_string.endswith('Try "yoda url --help" for more info'))