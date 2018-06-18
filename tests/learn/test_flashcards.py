# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner
import time

import tempfile
import os

import yoda
from modules import config


class TestFlashCard(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: url
    """

    def __init__(self, methodName='runTest'):
        super(TestFlashCard, self).__init__()
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
        #Test create set

        def testCreateSet():
            result = self.runner.invoke(yoda.cli, ['flashcards', 'sets', 'new', '1', ], input='test set')
            self.assertEqual(result.exit_code, 0)

        # Test set select
        def testSetSelect():
            result = self.runner.invoke(yoda.cli, ['flashcards', 'select', '1'], )
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode('ascii', 'ignore'))
            self.assertEqual(type(output_string), str)

        #Test list available sets
        def testShowAvaialableSets():
            result = self.runner.invoke(yoda.cli, ['flashcards', 'sets', 'list'])
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode('ascii', 'ignore'))
            self.assertEqual(type(output_string), str)

        # Test creation of cards
        def testCardCreation():
            result = self.runner.invoke(yoda.cli, ['flashcards', 'cards', 'add', 'test'], input='test card\n\n')
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode('ascii', 'ignore'))
            self.assertEqual(type(output_string), str)

        #Test selected set status
        def testSetStatus():
            result = self.runner.invoke(yoda.cli, ['flashcards', 'status',])
            self.assertEqual(result.exit_code, 0)
            output_string = str(result.output.encode('ascii', 'ignore'))
            self.assertEqual(type(output_string), str)



        testCreateSet()
        testSetSelect()
        testShowAvaialableSets()
        testSetStatus()
        testCardCreation()
        testSetStatus()