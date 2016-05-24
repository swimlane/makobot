# -*- coding: utf-8 -*-

import logging

from makobot import slackbot_settings as settings
from makobot.libs.xforce import XForce

from .base import Plugin
from .extractor import IPExtractor, MD5Extractor, URLExtractor
from .manager import plugin_manager

logger = logging.getLogger(__name__)


class XForcePlugin(Plugin):
    @property
    def enabled(self):
        return settings.XFORCE_API_KEY is not None and \
            settings.XFORCE_PASSWORD is not None

    def activate(self):
        logger.debug('Activating %s' % self.__class__.__name__)
        self.service = XForce(
            settings.XFORCE_API_KEY,
            settings.XFORCE_PASSWORD)

    def threshold_met(self, report):
        return 'score' in report and report['score'] >= 3

    def react(self):
        if not any(self.reports.values()):
            return
        score = max([r['score'] for r in self.reports.values()
                     if r and 'score' in r])
        return self.reaction(score)

    def reaction(self, score):
        if score < 2:
            return 'sunny'
        elif 2 >= score < 3:
            return 'mostly_sunny'
        elif 3 >= score < 4:
            return 'partly_sunny'
        elif 4 >= score < 5:
            return 'barely_sunny'
        elif 5 >= score < 6:
            return 'cloud'
        elif 6 >= score < 7:
            return 'rain_cloud'
        elif 7 >= score < 8:
            return 'thunder_cloud_and_rain'
        elif 8 >= score < 9:
            return 'lightning'
        elif score >= 9:
            return 'tornado'

    def risk_level(self, score):
        try:
            score = float(score)
        except TypeError:
            return 'UNKNOWN'

        if score < 2:
            return 'VERY LOW'
        elif 2 <= score < 3:
            return 'LOW'
        elif 3 <= score < 5:
            return 'MODERATE'
        elif 5 <= score < 8:
            return 'HIGH'
        elif score >= 8:
            return 'VERY HIGH'


class XForceIPPlugin(IPExtractor, XForcePlugin):
    def retrieve(self):
        for ip in self.reports:
            try:
                self.reports[ip] = self.service.ip(ip)
            except Exception as e:
                logger.debug('Error retrieving IP report for %s: %s' % (
                    ip, str(e)))
                continue

    def format(self, subject, report):
        result = []
        result.append('X-Force IP report for %s' % subject)
        if 'score' in report:
            result.append('Score: %s' % report['score'])
            result.append('Risk Level: %s' % self.risk_level(report['score']))
        if 'reason' in report:
            result.append('Reason: %s' % report['reason'])
        if 'cats' in report and report['cats']:
            result.append('Categories: %s' % ', '.join([
                '%s (%s)' % (k, v) for k, v in report['cats'].items()]))
        return ' '.join(result)


class XForceMD5Plugin(MD5Extractor, XForcePlugin):
    def retrieve(self):
        for md5 in self.reports:
            try:
                report = self.service.md5(md5)
            except Exception as e:
                logger.error('Error retrieving MD5 report for %s: %s' % (
                    md5, str(e)))
                continue
            if 'malware' in report:
                self.reports[md5] = report['malware']

    def format(self, subject, report):
        result = []
        result.append('X-Force MD5 report for %s' % subject)
        if 'family' in report:
            result.append('Malware Family: %s' % ', '.join(report['family']))
        if 'risk' in report:
            result.append('Risk: %s' % report['risk'])
        return ' '.join(result)

    def threshold_met(self, report):
        return True

    def react(self):
        if not any(self.reports.values()):
            return
        return 'lightning'


class XForceURLPlugin(URLExtractor, XForcePlugin):
    def retrieve(self):
        for url in self.reports:
            try:
                report = self.service.url(url)
            except Exception as e:
                logger.error('Error retrieving URL report for %s: %s' % (
                    url, str(e)))
                continue
            if 'result' in report:
                self.reports[url] = report['result']

    def format(self, subject, report):
        result = []
        result.append('X-Force URL report for %s' % subject)
        if 'score' in report:
            result.append('Score: %s' % report['score'])
            result.append('Risk Level: %s' % self.risk_level(report['score']))
        if 'reason' in report:
            result.append('Reason: %s' % report['reason'])
        if 'cats' in report and report['cats']:
            result.append('Categories: %s' % ', '.join([
                k for k, v in report['cats'].items()]))
        return ' '.join(result)


# Register Plugins
plugin_manager.register('ip', XForceIPPlugin)
plugin_manager.register('md5', XForceMD5Plugin)
plugin_manager.register('url', XForceURLPlugin)
