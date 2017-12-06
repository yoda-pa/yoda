# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestChat(TestCase):
    """
        Test for the following commands:

        | Module: chat
        | command: chat
    """

    def __init__(self, methodName='runTest'):
        super(TestChat, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ['chat', 'hello'])
        self.assertEqual(result.exit_code, 0)
