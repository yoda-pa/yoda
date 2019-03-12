# coding=utf-8
import unittest
from click.testing import CliRunner

import yoda


class TestWeather(unittest.TestCase):
    """
        Test for the following commands:

        | Module: weather 
        | command: weather 
    """

    def __init__(self, methodName="runTest"):
        super(TestWeather, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # testing for working weather service call
        result = self.runner.invoke(yoda.cli, ["weather", "new york"])
        self.assertEqual(result.exit_code, 0)

        # testing that the correct info is pulled for the correct location

        city = "Mexico City"
        result = self.runner.invoke(yoda.cli, ["weather", city])
        self.assertTrue("Mexico+City".lower() in result.output.lower())

        city = "Tokyo"
        result = self.runner.invoke(yoda.cli, ["weather", city])
        self.assertTrue(city.lower() in result.output.lower())

        city = "Belleville Ontario"
        result = self.runner.invoke(yoda.cli, ["weather", city])
        self.assertTrue("Belleville+Ontario".lower() in result.output.lower())


if __name__ == "__main__":
    unittest.main()
