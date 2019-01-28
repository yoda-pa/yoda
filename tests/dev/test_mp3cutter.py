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

    def __init__(self, methodName="runTest"):
        super(TestMpCutter, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        resources = os.path.dirname(sys.modules["yoda"].__file__)
        resources = resources + "/resources"

        mp3_location = resources + "/test.mp3"
        result = self.runner.invoke(
            yoda.cli, ["dev", "mp3cutter", mp3_location], input="y"
        )

        self.assertTrue("test_cropped.mp3" in os.listdir(resources))

        # Delete cropped mp3 file to delete unused file and clear up some space
        os.remove(mp3_location.replace("test.mp3", "test_cropped.mp3"))

        # Test for wrong file PATH
        result = self.runner.invoke(yoda.cli, ["mp3cutter", "no_file.mp3"])
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()

        # Test for wrong file format
        result = self.runner.invoke(yoda.cli, ["mp3cutter", "logo.png"])
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()

        # Test for endpoint greater than lenght of music
        result = self.runner.invoke(
            yoda.cli, ["mp3cutter", mp3_location, "10", "90000"]
        )
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()

        # Test for startpoint is greater than endpoint
        result = self.runner.invoke(
            yoda.cli, ["mp3cutter", mp3_location, "90000", "90"]
        )
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()

        # Test for startpoint greater than the lenght of music
        result = self.runner.invoke(
            yoda.cli, ["mp3cutter", mp3_location, "1000", "1001"]
        )
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
