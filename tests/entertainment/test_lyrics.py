# coding=utf-8
import unittest
from click.testing import CliRunner

import yoda


class TestLyrics(unittest.TestCase):
    """
        Test for the following commands:

        | Module: entertainment
        | command: lyrics
    """

    def __init__(self, arg):
        super(TestLyrics, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(
            yoda.cli, ["lyrics"], input="Coldplay\nAdventure of a Lifetime"
        )
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(yoda.cli, ["lyrics"], input="None\nNone")
        self.assertEqual(result.exit_code, 0)
