import os
import unittest

from makobot.libs.xforce import XForce


class XForceTestCase(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv('XFORCE_API_KEY')
        api_password = os.getenv('XFORCE_PASSWORD')
        if not api_key or not api_password:
            raise unittest.SkipTest(
                'XFORCE_API_KEY and XFORCE_API_PASSWORD environment '
                'variables must be set to run this test')
        self.xforce = XForce(api_key, api_password)

    def test_ip(self):
        result = self.xforce.ip('8.8.8.8')
        self.assertIn('ip', result)
        self.assertIn('reason', result)
        self.assertIn('cats', result)
        self.assertIn('score', result)

    def test_md5(self):
        result = self.xforce.md5('44d88612fea8a8f36de82e1278abb02f')
        result = result['malware']
        self.assertIn('md5', result)
        self.assertIn('risk', result)

    def test_url(self):
        result = self.xforce.url('http://thepiratebay.se')
        result = result['result']
        self.assertIn('url', result)
        self.assertIn('score', result)
        self.assertIn('cats', result)
