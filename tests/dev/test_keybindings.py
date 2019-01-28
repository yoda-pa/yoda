# coding=utf-8
from builtins import str
from unittest import TestCase
from click.testing import CliRunner

import pandas as pd
import os
import yoda


class TestKeybindings(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: url
    """

    def __init__(self, methodName="runTest"):
        super(TestKeybindings, self).__init__()
        self.runner = CliRunner()

    def runTest(self):

        test_keybinding_filepath = "tests/resources/test_software_kb.csv"
        d = {"actions": ["action1", "action2"], "keys": ["k1", "k2"]}
        pd.DataFrame(data=d).to_csv(test_keybinding_filepath, index=None, header=None)

        # add keybindings importing through a file
        result = self.runner.invoke(
            yoda.cli, ["keybindings", "add", "test_software", test_keybinding_filepath]
        )
        self.assertEqual(result.exit_code, 0)

        # Software Keybinding file already exists
        result = self.runner.invoke(
            yoda.cli, ["keybindings", "add", "test_software", test_keybinding_filepath]
        )
        self.assertEqual(result.exit_code, 0)

        os.remove(test_keybinding_filepath)

        # Software Keybinding file doesn't exist
        result = self.runner.invoke(
            yoda.cli, ["keybindings", "search", "t-test_software", "action1"]
        )
        self.assertEqual(result.exit_code, 0)

        # Software Keybinding file exist
        result = self.runner.invoke(
            yoda.cli, ["keybindings", "search", "test_software", "action1"]
        )
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    import unittest

    unittest.main()
