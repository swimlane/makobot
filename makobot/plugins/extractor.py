# -*- coding: utf-8 -*-

import re

from makobot.utils import clean_url, host_only


class EmailExtractor(object):
    REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')

    def extract(self, message):
        """Extracts the email addresses contained within the message text."""
        self.reports = dict([(email, None) for email in self.REGEX.findall(
            message.body.get('text', ''))])


class HostExtractor(object):
    REGEX = re.compile(r'(?:https?://[^\s\|]+)')

    def extract(self, message):
        """Extracts the hosts contained within the message text."""
        self.reports = dict([(host_only(h), None) for h in self.REGEX.findall(
            message.body.get('text', ''))])


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
    REGEX = re.compile(r'(?:https?://[^\s\|]+)')

    def extract(self, message):
        """Extracts the URLs contained within the message text"""
        text = message.body.get('text', '')
        self.reports = dict([(clean_url(url), None)
                             for url in self.REGEX.findall(text)])
