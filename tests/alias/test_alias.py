# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestAlias(TestCase):
    """
        Test for the following commands:

        | Module: alias
    """

    def __init__(self, methodName='runTest'):
        super(TestAlias, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        def test_new():
            result = self.runner.invoke(yoda.cli, ['alias', 'new'], orig_cmd="flashcards set new", alias_cmd="fsn")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'new'], orig_cmd="speedtest", alias_cmd="st")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'new'], orig_cmd="select", alias_cmd="s")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'new'], orig_cmd="alias", alias_cmd="a")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'new'], input="chat how are you", alias_cmd="c")
            self.assertEqual(0, result.exit_code)

        def test_aliasing():
            result = self.runner.invoke(yoda.cli, ['fsn'], domain="english")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['flashcards', 's'], domain="english")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['st'])
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['c'])
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['a', 'new'], orig_cmd="flashcards", alias_cmd="f")
            self.assertEqual(0, result.exit_code)

        def test_show():
            result = self.runner.invoke(yoda.cli, ['alias', 'show'])
            self.assertEqual(0, result.exit_code)

        def test_delete():
            result = self.runner.invoke(yoda.cli, ['alias', 'delete'], alias="fsn")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'delete'], alias="st")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'delete'], alias="s")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'delete'], alias="c")
            self.assertEqual(0, result.exit_code)
            result = self.runner.invoke(yoda.cli, ['alias', 'delete'], alias="")
            self.assertEqual(0, result.exit_code)

        test_new()
        test_aliasing()
        test_delete()
