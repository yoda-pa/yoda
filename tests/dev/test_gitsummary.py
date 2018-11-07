import sys
from unittest import TestCase
import mock
from functools import wraps
from click.testing import CliRunner

# def mock_decorator(*args, **kwargs):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

# mock.patch('click.group', mock_decorator).start()
# # mock.patch('de.group', lambda: x).start()
# # mock.patch('click.argument', lambda x: x).start()

import yoda
import github



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

        @mock.patch('yoda.dev.gitsummary')
        def testCalledWithProperArgs(mock_gitsummar):
            yoda.dev.gitsummary('abc', 'def')
            mock_gitsummar.assert_called_with('abc', 'def')

        # @mock.patch.object(github, 'Github', autospec=True)
        # def testStatisticCounting(mock_githublib):
        #     mock_githublib.return_value = True
        #     # mock_githublib.Github.return_value = True
        #     result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )
        #     # yoda.dev.gitsummary(github_login='a', github_password='b')

        #     mock_githublib.assert_called_with('login', 'password')
        #     self.assertTrue(mock_githublib.called)

        @mock.patch('yoda.dev.githublib')
        def testIssuesAndPrCounting(mock_gh):
            # prop = mock.PropertyMock(return_value='USER')
            mock_gh.Github.get_user.login = mock.PropertyMock(return_value=[])

            result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )
            self.assertEqual(result.output, 'abc')


        # @mock.patch('github')
        # def testIssuesAndPrCounting(mock_githublib):

        #     l = mock.PropertyMock(return_value='OK')
        #     u = mock.MagicMock()
        #     u.get_user.return_value = l
        #     mock_githublib.return_value = u


        #     # issue = mock.MagicMock()
        #     # issue.pull_request = False
        #     # pr = mock.MagicMock()
        #     # pr.pull_request = True
        #     # mock_githublib.search_issues = [issue, issue,pr, pr]



        #     # mock_githublib.get_user.return_value = l

        #     result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )

        #     # self.assertTrue(mock_githublib.search_issues.called)
        #     self.assertEqual(result.output, 'abc')



        # def testIssuesAndPrCounting(mock_counter):
        #     with patch('yoda.dev.gitsummary.number_of_issues_and_pull_requests')
        #     mock_counter.return_value = 3, 2
        #     # mock_counter.Github.return_value = True
        #     result = self.runner.invoke(yoda.cli, ['gitsummary', 'login', 'password', ], )
        #     mock_counter.assert_called_with('login', 'password')
        #     self.assertTrue(mock_counter.called)









        testExitingWithBadCredentials()
        testCalledWithProperArgs()
        # testStatisticCounting()
        testIssuesAndPrCounting()

