# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestIdeas(TestCase):
    """
        Test for the following commands:

        | Module: ideas
        | command: ideas
    """

    def __init__(self, methodName='runTest'):
        super(TestIdeas, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        project_name = 'dummy project'

        def _cleanup():
            result = self.runner.invoke(
                yoda.cli, ['ideas', 'remove', '--project', project_name])
            self.assertEqual(result.exit_code, 0)

        def testShowIdeas():
            result = self.runner.invoke(yoda.cli, ['ideas', 'show'])
            self.assertEqual(result.exit_code, 0)

        def testAddIdeaWithoutProject():
            result = self.runner.invoke(
                yoda.cli, ['ideas', 'add', '--task', 'task name'])

            self.assertEqual(result.output,
                             'Operation aborted. You have not selected any project or task. Please use this command with either --project or --inside flag\n'
                             )
            self.assertEqual(result.exit_code, 0)

        def testAddIdea():
            result = self.runner.invoke(
                yoda.cli, ['ideas', 'add', '--task', 'test', '--inside', project_name], input='test description'.encode('ascii', 'ignore'))
            print(result)
            # <Result TypeError('write() argument must be str, not bytes',)>
            self.assertEqual(result.output.encode('ascii', 'ignore'),
                             'Brief desc of the current task : \n'.encode('ascii', 'ignore')
                             )
            self.assertEqual(result.exit_code, 0)

        def testRemoveTaskFromProjectIdea():
            result = self.runner.invoke(
                yoda.cli, ['ideas', 'remove', '--task', 'test', '--inside', project_name], input='test description'.encode('ascii', 'ignore'))
            self.assertEqual(result.output.encode('ascii', 'ignore'),
                             'Task deleted successfully.\n'.encode('ascii', 'ignore')
                             )
            self.assertEqual(result.exit_code, 0)

        def testRemoveProjectIdea():
            result = self.runner.invoke(
                yoda.cli, ['ideas', 'remove', '--project', project_name])
            self.assertAlmostEqual(
                result.output.encode('ascii', 'ignore'),
                'Project deleted successfully.\n'.encode('ascii', 'ignore'))
            self.assertEqual(result.exit_code, 0)

        testShowIdeas()
        testAddIdea()
        testAddIdeaWithoutProject()
        testRemoveTaskFromProjectIdea()
        testRemoveProjectIdea()
