import unittest
from click.testing import CliRunner
import yoda


class PortScanTest(unittest.TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: portscan
      """

    def __init__(self, methodName="runTest"):
        super(PortScanTest, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(
            yoda.cli, ["dev", "portscan"], input="manparvesh.com"
        )
        self.assertIsNone(result.exception)
