import unittest
import yoda
from click.testing import CliRunner

import tempfile
import os

import yoda
from modules import config

class TestSuggestDrink(unittest.TestCase):
    """
    Test for the following commands:

        | Module: food
        | command: suggest_drinks
    """
    def __init__(self, methodName='runTest'):
        super(TestSuggestDrink, self).__init__()
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
        #Test Drink Suggestion
        result = self.runner.invoke(yoda.cli, ['food', 'suggest_drinks'])
        self.assertIsNone(result.exception)