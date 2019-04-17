# coding=utf-8
import mock
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

    @mock.patch('modules.weather.get_weather')
    def runTest(self, get_weather):
        city = "new york"
        expected_call = "new york "
        result = self.runner.invoke(yoda.cli, ["weather", city])
        get_weather.assert_called_once_with(expected_call)
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
