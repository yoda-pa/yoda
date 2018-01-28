# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestSpeedtest(TestCase):
    """
        Test for the following commands:

        | Module: dev
        | command: url
    """

    def __init__(self, methodName='runTest'):
        super(TestSpeedtest, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # todo
        pass