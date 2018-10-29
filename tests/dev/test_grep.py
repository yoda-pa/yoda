# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import os
import yoda


class TestGrepSingleFile(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: grep
    """

    def __init__(self, methodName="runTest"):
        super(TestGrepSingleFile, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        with self.runner.isolated_filesystem():
            with open("inputfile.txt", "w") as outfile:
                outfile.write(
                    "test should match\ntesT should match\nThistestshouldmatch\n"
                )
            result = self.runner.invoke(
                yoda.cli, ["dev", "grep", "test", "inputfile.txt", "-i", "True"]
            )
            output_string = result.output
            expected_output = (
                "test should match\ntesT should match\nThistestshouldmatch\n"
            )
            self.assertTrue(output_string == expected_output)


class TestGrepEntireFolder(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: grep
    """

    def __init__(self, methodName="runTest"):
        super(TestGrepEntireFolder, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        with self.runner.isolated_filesystem():
            with open("inputfile1.txt", "w") as outfile1:
                outfile1.write("tesT should not match\ntest should match")
            with open("inputfile2.txt", "w") as outfile2:
                outfile2.write("Thistestshouldmatch\n")

            result = self.runner.invoke(yoda.cli, ["dev", "grep", "test", os.getcwd()])
            output_string = result.output
            # Order changes from between machines. Need to either both possibilities.
            self.assertTrue(
                output_string == "Thistestshouldmatch\ntest should match"
                or output_string == "test should matchThistestshouldmatch\n"
            )
