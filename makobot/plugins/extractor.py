import re

from makobot.utils import clean_url


class IPExtractor(object):
    REGEX = re.compile(
        r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})')

    def extract(self, message):
        """Extracts the IPs contained within the message text."""
        self.reports = dict([(ip, None) for ip in self.REGEX.findall(
            message.body.get('text', ''))])


class MD5Extractor(object):
    REGEX = re.compile(r'([a-fA-F\d]{32})')

    def extract(self, message):
        """Extracts all the MD5 checksums found in a message"""
        self.reports = dict([(md5, None) for md5 in self.REGEX.findall(
            message.body.get('text', ''))])


class URLExtractor(object):
    REGEX = re.compile(r'(?:https?://[^\s]+)')

    def extract(self, message):
        """Extracts the URLs contained within the message text"""
        text = message.body.get('text', '')
        self.reports = dict([(clean_url(url), None)
                             for url in self.REGEX.findall(text)])