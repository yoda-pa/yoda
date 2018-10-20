import unittest
from click.testing import CliRunner
import yoda
import os
import sys

class TestMpCutter(unittest.TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: portscan
    """

    def __init__(self, methodName='runTest'):
        super(TestMpCutter, self).__init__()
        self.runner = CliRunner()


    def runTest(self):
        resources = os.path.dirname(sys.modules['yoda'].__file__)
        resources = resources + '/resources'

        mp3_location = resources + '/test.mp3'
        result = self.runner.invoke(yoda.cli, ['dev', 'mp3cutter', mp3_location])

        self.assertTrue("test_cropped.mp3" in os.listdir(resources))

        # Delete cropped mp3 file to delete unused file and clear up some space
        os.remove(mp3_location.replace("test.mp3", "test_cropped.mp3"))
