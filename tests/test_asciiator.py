from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestAsciiator(TestCase):
    def __init__(self, methodName="runTest"):
        super(TestAsciiator, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["ascii_transform", "tests/logo.png"])
        self.assertEqual(result.exit_code, 0)
