from unittest import TestCase
from click.testing import CliRunner
import yoda


class GitSummaryTest(TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: gitsummary
      """

    def __init__(self, methodName='runTest'):
        super(GitSummaryTest, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        def testExitingWithBadCredentials():
            result = self.runner.invoke(yoda.cli, ['gitsummary', 'bad_username', 'bad_password', ], )
            self.assertEqual(result.exit_code, 1)

        testExitingWithBadCredentials()
