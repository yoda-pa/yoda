import sys
from functools import wraps
from unittest import TestCase

import github
import mock
import yoda
from click.testing import CliRunner


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
            result = self.runner.invoke(
                yoda.cli, ['gitsummary', 'bad_username', 'bad_password', ], )
            self.assertEqual(result.exit_code, 1)

        @mock.patch.object(github, 'Github', autospec=True)
        def testCommandGetsCalled(mock_githublib):
            mock_githublib.return_value = True
            result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )

            mock_githublib.assert_called_with('login', 'password')
            self.assertTrue(mock_githublib.called)

        @mock.patch.object(github, 'Github', autospec=True)
        def testGettingLogin(mock_gh):
            # Mocking username
            type(mock_gh().get_user()).login = mock.PropertyMock(return_value='TestUser')

            result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )
            self.assertIn('TestUser, ready your GitHub statistics are', result.output)

        @mock.patch.object(github, 'Github', autospec=True)
        def testIssuesAndPrCounting(mock_gh):
            # Mocking issues and pull requests - expecting 3 issues, 2 PR
            issue = mock.MagicMock()
            pull_request = mock.MagicMock()
            type(issue).pull_request = mock.PropertyMock(return_value=False)
            type(pull_request).pull_request = mock.PropertyMock(return_value=True)
            mock_gh().search_issues.return_value = [issue, issue, issue, pull_request, pull_request]

            result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )
            self.assertIn('2 pull requests(s)', result.output)
            self.assertIn('3 issue(s)', result.output)

        @mock.patch.object(github, 'Github', autospec=True)
        def testReposAndCommitsCounting(mock_gh):
            # Mocking repos and commits - expecting 2 repos, 30 commits (2 repos * 3 branches * 5 commits)
            repo = mock.MagicMock()
            branch = mock.MagicMock()
            commit = mock.MagicMock()
            type(commit).sha = mock.PropertyMock(side_effect=(i for i in range(60)))

            mock_gh().get_user().get_repos.return_value = [repo for _ in range(2)]
            repo.get_branches.return_value = [branch for _ in range(3)]
            repo.get_commits.return_value = [commit for _ in range(5)]

            result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )
            self.assertIn('2 repositories', result.output)
            self.assertIn('30 commit(s)', result.output)

        testExitingWithBadCredentials()
        testCommandGetsCalled()
        testGettingLogin()
        testIssuesAndPrCounting()
        testReposAndCommitsCounting()
