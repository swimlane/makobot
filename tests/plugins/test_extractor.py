import unittest

from makobot.plugins.extractor import IPExtractor, MD5Extractor, URLExtractor


class IPExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = IPExtractor()

    def test_extract(self):
        class Message(object):
            body = {'text': '123.123.123.123 8.8.4.4 127.0.0.1'}
        self.extractor.extract(Message())
        self.assertEqual(self.extractor.ips, set(['123.123.123.123', '8.8.4.4',
                                      '127.0.0.1']))


class MD5ExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = MD5Extractor()

    def test_extract(self):
        class Message(object):
            body = {'text': '44d88612fea8a8f36de82e1278abb02f'}
        self.extractor.extract(Message())
        self.assertEqual(
            self.extractor.md5s,
            set(['44d88612fea8a8f36de82e1278abb02f']))


class URLExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = URLExtractor()

    def test_extract(self):
        class Message(object):
            body = {'text': 'https://www.thepiratebay.se/uri/to/something'}
        self.extractor.extract(Message())
        self.assertEqual(
            self.extractor.urls,
            set(['https://www.thepiratebay.se']))
