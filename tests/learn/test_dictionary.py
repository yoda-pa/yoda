# coding=utf-8
from builtins import str
from mock import patch
from unittest import TestCase
from click.testing import CliRunner

import yoda


class TestDictionary(TestCase):
    """
        Test for the following commands:

        | Module: learn
        | command: define, synonym, antonym, example
    """
    DICTIONARY_RESPONSE = {
        u'word': u'fat',
        u'definitions': [
            {u'definition': u'make fat or plump', u'partOfSpeech': u'verb'},
            {u'definition': u'lucrative', u'partOfSpeech': u'adjective'},
            {u'definition': u'marked by great fruitfulness',
                            u'partOfSpeech': u'adjective'},
            {u'definition': u'excess bodily weight', u'partOfSpeech': u'noun'},
        ],
        u'synonyms': [
            u'fatten', u'fatten out', u'fatten up', u'fill out', u'flesh out',
            u'plump', u'plump out', u'juicy', u'fertile', u'productive',
            u'rich', u'avoirdupois', u'blubber', u'fatness', u'adipose tissue',
            u'fatty tissue', u'fatty'],
        u'antonyms': [u'thin'],
        u'examples': [
            u'a nice fat job', u'a fat land', u'fatty food', u'fat tissue',
            u'she disliked fatness in herself as well as in others',
            u'fatty tissue protected them from the severe cold', u'a fat rope'
            u'pizza has too much fat', u'he hadn\'t remembered how fat she was'
        ]
    }

    def __init__(self, methodName="runTest"):
        super(TestDictionary, self).__init__()
        self.runner = CliRunner()

    @patch('modules.learn.requests')
    def runTest(self, requests):
        requests.get.json.return_value = self.DICTIONARY_RESPONSE
        result = self.runner.invoke(yoda.cli, ["dictionary", "define", "fat"])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode("ascii", "ignore"))
        self.assertEqual(type(output_string), str)

        result = self.runner.invoke(yoda.cli, ["dictionary", "synonym", "fat"])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode("ascii", "ignore"))
        self.assertEqual(type(output_string), str)

        result = self.runner.invoke(yoda.cli, ["dictionary", "antonym", "fat"])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode("ascii", "ignore"))
        self.assertEqual(type(output_string), str)

        result = self.runner.invoke(yoda.cli, ["dictionary", "example", "fat"])
        self.assertEqual(result.exit_code, 0)
        output_string = str(result.output.encode("ascii", "ignore"))
        self.assertEqual(type(output_string), str)
