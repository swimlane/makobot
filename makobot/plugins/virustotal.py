from __future__ import division

import logging

from makobot import slackbot_settings as settings
from makobot.libs.virustotal import VirusTotal

from .base import Plugin
from .extractor import IPExtractor, MD5Extractor, URLExtractor
from .manager import plugin_manager

logger = logging.getLogger(__name__)


class VirusTotalPlugin(Plugin):
    @property
    def enabled(self):
        return settings.VIRUSTOTAL_API_KEY is not None

    def activate(self):
        self.service = VirusTotal(settings.VIRUSTOTAL_API_KEY)


class VirusTotalIPPlugin(IPExtractor, VirusTotalPlugin):
    def retrieve(self):
        for ip in self.reports:
            try:
                report = self.service.ip(ip)
            except Exception as e:
                logger.debug('Error retrieving IP report for %s: %s' % (
                    ip, e.message))
                continue
            if 'response_code' in report and report['response_code'] == 1:
                self.reports[ip] = report

    def format(self, subject, report):
        result = []
        result.append('VirusTotal IP report for %s' % subject)
        if 'as_owner' in report:
            result.append('Owner: %s' % report['as_owner'])
        if 'detected_referrer_samples' in report:
            samples = report['detected_referrer_samples']
            positives = sum([s['positives'] for s in samples])
            total = sum([s['total'] for s in samples])
            percentage = '{:.1%}'.format(positives / total)
            result.append('Positives: %s/%s (%s)' % (
                positives, total, percentage))
        return ' '.join(result)

    def threshold_met(self, report):
        if 'detected_referrer_samples' not in report:
            return False
        samples = report['detected_referrer_samples']
        return sum([s['positives'] for s in samples]) > 0

    def react(self, message):
        if not any(self.reports.values()):
            message.react('fog')
            return
        positives = 0
        for subject, report in self.reports.items():
            samples = report.get('detected_referrer_samples', [])
            positives += sum([s['positives'] for s in samples])
        if positives > 0:
            message.react('lightning')


class VirusTotalMD5Plugin(MD5Extractor, VirusTotalPlugin):
    def retrieve(self):
        for md5 in self.reports:
            try:
                report = self.service.md5(md5)
            except Exception as e:
                logger.error('Error retrievingMD5 report for %s: %s' % (
                    md5, e.message))
                continue
            if 'response_code' in report and report['response_code'] == 1:
                self.reports[md5] = report

    def format(self, subject, report):
        result = []
        result.append('VirusTotal Md5 report for %s' % subject)
        if 'positives' in report and 'total' in report:
            percentage = '{:.1%}'.format(report['positives'] / report['total'])
            result.append('Positives: %s/%s (%s)' % (
                report['positives'], report['total'], percentage))
        return ' '.join(result)

    def threshold_met(self, report):
        if 'positives' not in report:
            return False
        return report['positives'] > 0

    def react(self, message):
        if not any(self.reports.values()):
            message.react('fog')
            return
        positives = sum([r['positives'] for _, r in self.reports.items()
                         if 'positives' in r])
        if positives > 0:
            message.react('lightning')


class VirusTotalURLPlugin(URLExtractor, VirusTotalPlugin):
    def retrieve(self):
        for url in self.reports:
            try:
                report = self.service.url(url)
            except Exception as e:
                logger.error('Error retrieving URL report for %s: %s' % (
                    url, e.message))
                continue
            if 'response_code' in report and report['response_code'] == 1:
                self.reports[url] = report

    def format(self, subject, report):
        result = []
        result.append('VirusTotal URL report for %s' % subject)
        if 'positives' in report and 'total' in report:
            percentage = '{:.1%}'.format(report['positives'] / report['total'])
            result.append('Positives: %s/%s (%s)' % (
                report['positives'], report['total'], percentage))
        return ' '.join(result)

    def threshold_met(self, report):
        if 'positives' not in report:
            return False
        return report['positives'] > 0

    def react(self, message):
        if not any(self.reports.values()):
            message.react('fog')
            return
        positives = sum([r['positives'] for _, r in self.reports.items()
                         if 'positives' in r])
        if positives > 0:
            message.react('lightning')


# Register Plugins
plugin_manager.register('ip', VirusTotalIPPlugin)
plugin_manager.register('md5', VirusTotalMD5Plugin)
plugin_manager.register('url', VirusTotalURLPlugin)
