# coding=utf-8
from mock import patch
import unittest
from click.testing import CliRunner

import yoda

COLDPLAY_LYRICS = {
    'lyrics': ('Turn your magic on\nUmi she\'d say\nEverything you want\'s a'
               'dream away\nAnd we are legends every day\nThat\'s what she told'
               'me\n\nTurn your magic on\nTo me she\'d say\nEverything you '
               'want\'s a dream away\nUnder this pressure, under this weight..')
}
NO_LYRICS_FOUND = {'error': 'No lyrics found'}


class TestLyrics(unittest.TestCase):
    """
        Test for the following commands:

        | Module: entertainment
        | command: lyrics
    """

    def __init__(self, arg):
        super(TestLyrics, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        with patch('modules.entertainment.requests') as requests:
            requests.get().json.return_value = COLDPLAY_LYRICS
            result = self.runner.invoke(
                yoda.cli, ['lyrics'], input='Coldplay\nAdventure of a Lifetime'
            )
            output_string = str(
                result.output.encode("ascii", "ignore").decode("utf-8")
            ).strip()
            self.assertIn('--------Lyrics--------', output_string)
            self.assertEqual(result.exit_code, 0)

        with patch('modules.entertainment.requests') as requests:
            requests.get().json.return_value = NO_LYRICS_FOUND
            result = self.runner.invoke(
                yoda.cli, ['lyrics'], input='None\nNone'
            )
            output_string = str(
                result.output.encode("ascii", "ignore").decode("utf-8")
            ).strip()
            self.assertIn('No lyrics found', output_string)
            self.assertEqual(result.exit_code, 0)
