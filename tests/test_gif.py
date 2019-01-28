# coding=utf-8
from unittest import TestCase
from click.testing import CliRunner

import os
import yoda


class TestGifMaker(TestCase):
    """
        Test for the following commands:

        | Module: gif
        | command: from_images
    """

    def __init__(self, methodName="runTest"):
        super(TestGifMaker, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        source = os.path.join(os.getcwd(), "tests/resources/gif_frames")
        with self.runner.isolated_filesystem():
            output = os.path.join(os.getcwd(), "test.gif")
            self.runner.invoke(
                yoda.cli,
                [
                    "gif",
                    "from-images",
                    "--source",
                    source,
                    "--output",
                    output,
                    "--fps",
                    "9",
                ],
            )
            self.assertTrue(os.path.isfile(output))
