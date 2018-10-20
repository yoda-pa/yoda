import unittest

from modules.dev import get_whois_data

class TestWhois(unittest.TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: whois
    """

    def __init__(self, methodName='runTest'):
        super(TestWhois, self).__init__()


    def runTest(self):
        request_code = get_whois_data("https://google.com")[1]
        self.assertTrue(request_code == 200)
