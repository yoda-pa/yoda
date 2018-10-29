import unittest

from click.testing import CliRunner
import yoda


class TestWhois(unittest.TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: whois
    """

    def __init__(self, methodName="runTest"):
        super(TestWhois, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(yoda.cli, ["whois", "https://google.com"])
        self.assertEqual(result.exit_code, 0)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()

        result = self.runner.invoke(
            yoda.cli, ["whois", "http://asdfghjklpoiuytrew.com/"]
        )
        self.assertEqual(result.exit_code, 1)
        output_string = str(
            result.output.encode("ascii", "ignore").decode("utf-8")
        ).strip()
