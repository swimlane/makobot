# -*- coding: utf-8 -*-

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

    def reaction(self, score):
        if score == 0:
            return 'sunny'
        elif 0 < score <= 0.02:
            return 'mostly_sunny'
        elif 0.02 < score <= 0.04:
            return 'partly_sunny'
        elif 0.04 < score <= 0.06:
            return 'barely_sunny'
        elif 0.06 < score <= 0.1:
            return 'cloud'
        elif 0.1 < score <= 0.15:
            return 'rain_cloud'
        elif 0.15 < score <= 0.2:
            return 'thunder_cloud_and_rain'
        elif 0.2 < score <= 0.8:
            return 'lightning'
        elif score > 0.8:
            return 'tornado'

    def risk_level(self, score):
        try:
            score = float(score)
        except TypeError:
            return 'UNKNOWN'

        if score == 0:
            return 'VERY LOW'
        elif 0 < score <= 0.02:
            return 'LOW'
        elif 0.02 < score <= 0.2:
            return 'MODERATE'
        elif 0.2 < score <= 0.8:
            return 'HIGH'
        elif score > 0.8:
            return 'VERY HIGH'


class VirusTotalIPPlugin(IPExtractor, VirusTotalPlugin):
    def retrieve(self):
        for ip in self.reports:
            try:
                report = self.service.ip(ip)
            except Exception as e:
                logger.debug('Error retrieving IP report for %s: %s' % (
                    ip, str(e)))
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
            percentage = '{:.1%}'.format(positives / total) if total else 'N/A'
            result.append('Positives: %s/%s (%s)' % (
                positives, total, percentage))
            risk_level = self.risk_level(positives / total) if total else 'N/A'
            result.append('Risk Level: %s' %
                          risk_level)
        return ' '.join(result)

    def threshold_met(self, report):
        if 'detected_referrer_samples' not in report:
            return False
        samples = report['detected_referrer_samples']
        return sum([s['positives'] for s in samples]) > 0

    def react(self):
        if not any(self.reports.values()):
            return
        positives = 0
        total = 0
        for subject, report in self.reports.items():
            samples = report.get('detected_referrer_samples', [])
            positives += sum([s['positives'] for s in samples])
            total += sum([s['total'] for s in samples])
        if not total:
            return
        return self.reaction(positives / total)


class VirusTotalMD5Plugin(MD5Extractor, VirusTotalPlugin):
    def retrieve(self):
        for md5 in self.reports:
            try:
                report = self.service.md5(md5)
            except Exception as e:
                logger.error('Error retrievingMD5 report for %s: %s' % (
                    md5, str(e)))
                continue
            if 'response_code' in report and report['response_code'] == 1:
                self.reports[md5] = report

    def format(self, subject, report):
        result = []
        result.append('VirusTotal Md5 report for %s' % subject)
        if 'positives' in report and 'total' in report:
            positives = report['positives']
            total = report['total']
            percentage = '{:.1%}'.format(positives / total) if total else 'N/A'
            result.append('Positives: %s/%s (%s)' % (
                positives, total, percentage))
            risk_level = self.risk_level(positives / total) if total else 'N/A'
            result.append('Risk Level: %s' %
                          risk_level)
        return ' '.join(result)

    def threshold_met(self, report):
        if 'positives' not in report:
            return False
        return report['positives'] > 0

    def react(self):
        if not any(self.reports.values()):
            return
        positives = sum([r['positives'] for _, r in self.reports.items()
                         if 'positives' in r])
        total = sum([r['total'] for _, r in self.reports.items()
                     if 'total' in r])
        if not total:
            return
        return self.reaction(positives / total)


class VirusTotalURLPlugin(URLExtractor, VirusTotalPlugin):
    def retrieve(self):
        for url in self.reports:
            try:
                report = self.service.url(url)
            except Exception as e:
                logger.error('Error retrieving URL report for %s: %s' % (
                    url, str(e)))
                continue
            if 'response_code' in report and report['response_code'] == 1:
                self.reports[url] = report

    def format(self, subject, report):
        result = []
        result.append('VirusTotal URL report for %s' % subject)
        if 'positives' in report and 'total' in report:
            positives = report['positives']
            total = report['total']
            percentage = '{:.1%}'.format(positives / total) if total else 'N/A'
            result.append('Positives: %s/%s (%s)' % (
                positives, total, percentage))
            risk_level = self.risk_level(positives / total) if total else 'N/A'
            result.append('Risk Level: %s' %
                          risk_level)
        return ' '.join(result)

    def threshold_met(self, report):
        if 'positives' not in report:
            return False
        return report['positives'] > 0

    def react(self):
        if not any(self.reports.values()):
            return
        positives = sum([r['positives'] for _, r in self.reports.items()
                         if 'positives' in r])
        total = sum([r['total'] for _, r in self.reports.items()
                     if 'total' in r])
        if not total:
            return
        return self.reaction(positives / total)


# Register Plugins
plugin_manager.register('ip', VirusTotalIPPlugin)
plugin_manager.register('md5', VirusTotalMD5Plugin)
plugin_manager.register('url', VirusTotalURLPlugin)
