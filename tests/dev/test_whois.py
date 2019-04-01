from mock import patch, PropertyMock
import unittest

from click.testing import CliRunner
import yoda


GOOGLE_WHOIS = (
    u'<!DOCTYPE HTML><html dir="ltr"><body class="home-bg"> Domain Information'
    u'</div><div class="df-label">Domain:</div><div class="df-value">google.com'
    u'</div></div><div class="df-label">Registrar:</div><div class="df-value"'
    u'>MarkMonitor Inc.</div><div class="df-label">Registered On:</div><div '
    u'class="df-value">1997-09-15</div><div class="df-label">Expires On:</div>'
    u'<div class="df-value">2020-09-13 </div><div class="df-label">Updated On:'
    u'</div><div class="df-value">2018-02-21</div> <div class="df-label">'
    u'Status:</div><div class="df-value">clientDeleteProhibited</div><div class'
    u'="df-label">Name Servers:</div><div class="df-value">ns1.google.com</div>'
    u'<div class="df-label">Organization:</div><div class="df-value">Google LLC'
    u'</div><div class="df-label">State:</div><div class=class="df-label">State'
    u':</div><div class="df-value">CA</div><div class="df-label">Country:</div>'
    u'<div class="df-value">US</div></div></div><div class="df-label"> '
    u'Organization:</div><div class="df-value">Google LLC</div><div class='
    u'"df-label">State:</div><div class="df-value">CA</div><div class="df-label'
    u'">Country:</div><div class="df-value">US</div<div class="df-label">'
    u'Organization:</div><div class="df-value">Google LLC</div><div class='
    u'"df-label">State:</div><div class="df-value">CA</div><div class="df-label'
    u'">Country:</div><div class="df-value">US</div></div></body></html>'
)


class TestWhois(unittest.TestCase):
    """
          Test for the following commands:

          | Module: dev
          | command: whois
    """

    def __init__(self, methodName="runTest"):
        super(TestWhois, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        with patch('modules.dev.requests') as requests:
            text_return_value = PropertyMock(return_value=GOOGLE_WHOIS)
            type(requests.get.return_value).text = text_return_value
            result = self.runner.invoke(
                yoda.cli, ["whois", "https://google.com"]
            )
            self.assertEqual(result.exit_code, 0)
            output_string = str(
                result.output.encode("ascii", "ignore").decode("utf-8")
            ).strip()
            self.assertIn('google.com', output_string)
            self.assertIn('Google LLC', output_string)

        with patch('modules.dev.requests') as requests:
            text_return_value = PropertyMock(return_value='')
            type(requests.get.return_value).text = text_return_value
            result = self.runner.invoke(
                yoda.cli, ["whois", "http://asdfghjklpoiuytrew.com/"]
            )
            self.assertEqual(result.exit_code, 1)
            output_string = str(
                result.output.encode("ascii", "ignore").decode("utf-8")
            ).strip()
            self.assertIn(
                'This domain has not been registered yet :/', output_string
            )
