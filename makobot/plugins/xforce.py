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
        self.xforce = XForce(settings.XFORCE_API_KEY, settings.XFORCE_PASSWORD)

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


class XForceIPReputationPlugin(IPExtractor, XForcePlugin):
    def report(self, message, active=True):
        self.retrieve_report()
        if not self.reports:
            message.reaction('fog')
            if active:
                message.reply('No IP reputation reports for %s' %
                              ', '.join(self.ips))
            return
        high_score = 1
        for report in self.reports:
            if active:
                message.reply(self.format_report(report))
            elif 'score' in report and report['score'] >= 3:
                message.send(self.format_report(report))
            if 'score' in report and report['score'] > high_score:
                high_score = report['score']
        message.reaction(self.reaction(high_score))

    def retrieve_report(self):
        self.reports = []
        for ip in self.ips:
            try:
                self.reports.append(self.xforce.ip(ip))
            except Exception:
                continue

    def format_report(self, report):
        result = []
        if 'ip' in report:
            result.append('X-Force IP Reputation for %s' % report['ip'])
        if 'score' in report:
            result.append('Score: %s' % report['score'])
            result.append('Risk Level: %s' % self.risk_level(report['score']))
        if 'reason' in report:
            result.append('Reason: %s' % report['reason'])
        if 'cats' in report and report['cats']:
            result.append('Categories: %s' % ', '.join([
                '%s (%s)' % (k, v) for k, v in report['cats'].items()]))
        return ' '.join(report)


class XForceMD5ReputationPlugin(MD5Extractor, XForcePlugin):
    def report(self, message, active=True):
        self.retrieve_report()
        if not self.reports:
            message.reaction('fog')
            if active:
                message.reply('No malware reports for %s' %
                              ', '.join(self.md5s))
            return
        for report in self.reports:
            message.reply(self.format_report(report))
            message.reaction('lightning')

    def retrieve_report(self):
        self.reports = []
        for md5 in self.md5s:
            try:
                self.reports.append(self.xforce.md5(md5))
            except Exception:
                break

    def format_report(self, report, inline=False):
        result = []
        if 'md5' in report:
            result.append('X-Force Malware Report for %s' % report['md5'])
        if 'family' in report:
            result.append('Malware Family: %s' % ', '.join(report['family']))
        if 'risk' in report:
            result.append('Risk: %s' % report['risk'])
        return ' '.join(report)


class XForceURLReputationPlugin(URLExtractor, XForcePlugin):
    def report(self, message, active=True):
        self.retrieve_report()
        if not self.reports:
            message.react('fog')
            if active:
                message.reply('No URL reputation reports for %s' %
                              ', '.join(self.urls))
            return
        high_score = 1
        for report in self.reports:
            if active:
                message.reply(self.format_report(report))
            elif 'score' in report and report['score'] >= 3:
                message.send(self.format_report(report))
            if 'score' in report and report['score'] > high_score:
                high_score = report['score']
        message.react(self.reaction(high_score))

    def retrieve_report(self):
        self.reports = []
        for url in self.urls:
            try:
                report = self.xforce.url(url)
            except Exception:
                break
            if 'result' in report:
                self.reports.append(report['result'])

    def format_report(self, report):
        result = []
        if 'url' in report:
            result.append('X-Force URL Reputation for %s' % report['url'])
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
plugin_manager.register('ip', XForceIPReputationPlugin)
plugin_manager.register('md5', XForceMD5ReputationPlugin)
plugin_manager.register('url', XForceURLReputationPlugin)
