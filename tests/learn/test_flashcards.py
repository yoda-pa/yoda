# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner
import time
import yoda


class TestFlashCard(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: url
    """

    def __init__(self, methodName="runTest"):
        super(TestFlashCard, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # Test create set

        def testCreateSet():
            result = self.runner.invoke(
                yoda.cli, ["flashcards", "sets", "new", "1"], input="test set"
            )
            self.assertEqual(result.exit_code, 0)

        # Test set select
        def testSetSelect():
            result = self.runner.invoke(yoda.cli, ["flashcards", "select", "1"])
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode("ascii", "ignore"))
            self.assertEqual(type(output_string), str)

        # Test list available sets
        def testShowAvaialableSets():
            result = self.runner.invoke(yoda.cli, ["flashcards", "sets", "list"])
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode("ascii", "ignore"))
            self.assertEqual(type(output_string), str)

        # Test creation of cards
        def testCardCreation():
            result = self.runner.invoke(
                yoda.cli, ["flashcards", "cards", "add", "test"], input="test card\n\n"
            )
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode("ascii", "ignore"))
            self.assertEqual(type(output_string), str)

        # Test selected set status
        def testSetStatus():
            result = self.runner.invoke(yoda.cli, ["flashcards", "status"])
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode("ascii", "ignore"))
            self.assertEqual(type(output_string), str)

        testCreateSet()
        testSetSelect()
        testShowAvaialableSets()
        testSetStatus()
        testCardCreation()
        testSetStatus()
