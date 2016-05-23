import mock
import unittest

from makobot.plugins.extractor import EmailExtractor, HostExtractor, \
    IPExtractor, MD5Extractor, URLExtractor


class EmailExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = EmailExtractor()

    def test_extract(self):
        mock_message = mock.Mock()
        mock_message.body = {'text': 'foo@bar.com info@google.com'}
        self.extractor.extract(mock_message)
        expected = {
            'foo@bar.com': None,
            'info@google.com': None}
        self.assertEqual(self.extractor.reports, expected)


class HostExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = HostExtractor()

    def test_extract(self):
        mock_message = mock.Mock()
        mock_message.body = {'text': 'http://www.google.com http://foo.bar.net'}
        self.extractor.extract(mock_message)
        expected = {
            'www.google.com': None,
            'foo.bar.net': None}
        self.assertEqual(self.extractor.reports, expected)


class IPExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = IPExtractor()

    def test_extract(self):
        mock_message = mock.Mock()
        mock_message.body = {'text': '123.123.123.123 8.8.4.4 127.0.0.1'}
        self.extractor.extract(mock_message)
        expected = {
            '123.123.123.123': None,
            '8.8.4.4': None,
            '127.0.0.1': None}
        self.assertEqual(self.extractor.reports, expected)


class MD5ExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = MD5Extractor()

    def test_extract(self):
        mock_message = mock.Mock()
        mock_message.body = {'text': '44d88612fea8a8f36de82e1278abb02f'}
        self.extractor.extract(mock_message)
        self.assertEqual(
            self.extractor.reports,
            {'44d88612fea8a8f36de82e1278abb02f': None})


class URLExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = URLExtractor()

    def test_extract(self):
        mock_message = mock.Mock()
        mock_message.body = {'text': 'https://www.thepiratebay.se/uri/to/something'}
        self.extractor.extract(mock_message)
        self.assertEqual(
            self.extractor.reports,
            {'https://www.thepiratebay.se': None})
