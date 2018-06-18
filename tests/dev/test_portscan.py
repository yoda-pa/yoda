import unittest
from click.testing import CliRunner

import tempfile
import os

import yoda
from modules import config

class PortScanTest(unittest.TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: portscan
      """

    def __init__(self, methodName='runTest'):
        super(PortScanTest, self).__init__()
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
        result = self.runner.invoke(yoda.cli, ['dev','portscan'],input='manparvesh.com')
        self.assertIsNone(result.exception)

import unittest
unittest.main()