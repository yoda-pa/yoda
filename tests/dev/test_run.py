# coding=utf-8
from mock import patch, Mock
from unittest import TestCase

from click.testing import CliRunner

import yoda


class TestRun(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: run
    """

    def __init__(self, methodName="runTest"):
        super(TestRun, self).__init__()
        self.runner = CliRunner()

    @patch('modules.dev.HackerEarthAPI')
    @patch('modules.dev.RunAPIParameters')
    def runTest(self, RunAPIParameters, HackerEarthAPI):
        mock_api_run_result = Mock()
        mock_api_run_result.__dict__['output'] = 'output'
        mock_api_run_result.__dict__['web_link'] = 'web_link'
        HackerEarthAPI().run.return_value = mock_api_run_result

        # Testing with existing file
        result = self.runner.invoke(yoda.cli, ["run", "tests/resources/test_code.py"])
        self.assertEqual(result.exit_code, 0)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
        expected_result = ('Compiling code..\nRunning code...\n'
                           'Output:\noutput\nLink: web_link')
        self.assertIn(output_string, expected_result)

        # Testing missing file
        result = self.runner.invoke(yoda.cli, ["run", "no_file.py"])
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
        expected_result = ('No file such as no_file.py, '
                           'Please re-check the file path and try again.')
        self.assertIn(output_string, expected_result)

        # Testing unsupported language
        result = self.runner.invoke(yoda.cli, ["run", "logo.png"])
        self.assertEqual(result.exit_code, -1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
        expected_result = 'Sorry, Unsupported language.'
        self.assertIn(output_string, expected_result)
