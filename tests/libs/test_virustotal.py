import os
import unittest

from makobot.libs.virustotal import VirusTotal


class VirusTotalTestCase(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv('VIRUSTOTAL_API_KEY')
        if not api_key:
            raise unittest.SkipTest(
                'VIRUSTOTAL_API_KEY environment variables '
                'must be set to run this test')
        self.virustotal = VirusTotal(api_key)

    def test_ip(self):
        result = self.virustotal.ip('8.8.8.8')
        self.assertIn('as_owner', result)
        self.assertIn('detected_referrer_samples', result)

    def test_md5(self):
        result = self.virustotal.md5('44d88612fea8a8f36de82e1278abb02f')
        self.assertIn('positives', result)
        self.assertIn('total', result)

    def test_url(self):
        result = self.virustotal.url('http://thepiratebay.se')
        self.assertIn('positives', result)
        self.assertIn('total', result)
