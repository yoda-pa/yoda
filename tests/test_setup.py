# coding=utf-8
import os
import shutil
from unittest import TestCase

from click.testing import CliRunner
from mock import patch

import yoda


class TestSetup(TestCase):
    """
        Test for the following commands:

        | Module: setup
        | command: setup
    """

    def __init__(self, methodName="runTest"):
        super(TestSetup, self).__init__()
        self.runner = CliRunner()

    def Newtest(self):
        """
        Test "yoda setup new"
        :return:
        """
        # Now 'setup new'. This tries to insert incorrect data to test the code fully
        result = self.runner.invoke(
            yoda.cli,
            ["setup", "new"],
            input="\n")
        self.assertIn('You entered nothing', result.output)

        # Test for invalid email
        result = self.runner.invoke(
            yoda.cli,
            ["setup", "new"],
            input="Name\nmyemail.com\n")
        self.assertIn('Invalid email ID', result.output)

        # Test for valid email
        result = self.runner.invoke(
            yoda.cli,
            ["setup", "new"],
            input="Name\nmy@email.com\n"
        )
        self.assertNotIn("Invalid email ID", result.output)

        result = self.runner.invoke(
            yoda.cli,
            ["setup", "new"],
            input="Name\nmy@email.com\n\n")
        self.assertIn('You entered nothing', result.output)

        with patch('getpass.getpass') as gp:
            gp.return_value = ""
            result = self.runner.invoke(
                yoda.cli,
                ["setup", "new"],
                input="Name\nmy@email.com\nGhUser\n\n")
            self.assertIn('You entered nothing', result.output)

        # test creating folder
        if os.path.exists(os.path.expanduser("~/.yodatest/")):
            shutil.rmtree(os.path.expanduser("~/.yodatest/"))

        with patch('getpass.getpass') as gp:
            gp.return_value = "GhPassword"
            result = self.runner.invoke(
                yoda.cli,
                ["setup", "new"],
                input="Name\nmy@email.com\nGhUser\n~/.yodatest/\nn\n~/.yodatest/\ny\n"
            )
        self.assertIn("Path doesn't exist! Do you want to create it?", result.output)
        self.assertIn("Folder created!", result.output)
        self.assertEqual(result.exit_code, 0)

        # test overwriting response NO
        with patch('getpass.getpass') as gp:
            gp.return_value = "GhPassword"
            result = self.runner.invoke(
                yoda.cli,
                ["setup", "new"],
                input="Name\nmy@email.com\nGhUser\n~/.yodatest/\nn\n"
            )
        self.assertIn("A setup configuration already exists. Are you sure you want to overwrite it?", result.output)
        self.assertEqual(result.exit_code, 0)

        # test overwriting response YES
        with patch('getpass.getpass') as gp:
            gp.return_value = "GhPassword"
            result = self.runner.invoke(
                yoda.cli,
                ["setup", "new"],
                input="Name\nmy@email.com\nGhUser\n~/.yodatest/\ny\n"
            )
        self.assertIn("A setup configuration already exists. Are you sure you want to overwrite it?", result.output)
        self.assertIn("Removed old setup configuration", result.output)
        self.assertEqual(result.exit_code, 0)

    def Deletetest(self):
        """
        Test "yoda setup delete"
        :return:
        """
        # Test delete()
        result = self.runner.invoke(
            yoda.cli,
            ["setup", "delete"],
            input="n\n"
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Operation cancelled", result.output)

        result = self.runner.invoke(
            yoda.cli,
            ["setup", "delete"],
            input="y\n"
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration file deleted", result.output)

    def Checktest(self, expectedoutput):
        """
        Test "yoda setup check"
        :param expectedoutput: 0 = Config. does NOT exist 1 = Config. Exists
        :return:
        """

        if expectedoutput == 0:
            result = self.runner.invoke(yoda.cli, ["setup", "check"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("The configuration file does not exist.", result.output)
            return

        if expectedoutput == 1:
            result = self.runner.invoke(yoda.cli, ["setup", "check"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Name: Name", result.output)
            self.assertIn("Email: my@email.com", result.output)
            self.assertIn("Github username: GhUser", result.output)

    def runTest(self):
        # If you use yoda in the same computer that you run this test
        # it will delete your current configuration
        # TODO: Make this run in a testing directory

        result = self.runner.invoke(yoda.cli, ["setup"])
        self.assertEqual(result.exit_code, 0)

        self.Newtest()
        self.Checktest(1)
        self.Deletetest()
        self.Checktest(0)
