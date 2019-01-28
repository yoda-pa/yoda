# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestHealth(TestCase):
    """
        Test for the following commands:

        | Module: health
        | command: health
    """

    def __init__(self, methodName="runTest"):
        super(TestHealth, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # result = self.runner.invoke(yoda.cli, ['rlist', 'view', 'opt'])
        # self.assertEqual(result.exit_code, 0)

        # result = self.runner.invoke(yoda.cli, ['rlist', 'add'], input="title\n_auth\n_kind\n_tags\n")
        # self.assertEqual(result.exit_code, 0)
        # output_string = str(result.output.encode('ascii', 'ignore'))
        # print(output_string)
        #
        # result = self.runner.invoke(yoda.cli, ['rlist', 'view'])
        # self.assertEqual(result.exit_code, 0)

        # todo
        pass
