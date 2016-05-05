import logging

from makobot import slackbot_settings as settings
from makobot.libs.virustotal import VirusTotal

from .base import Plugin
from .extractor import IPExtractor

logger = logging.getLogger(__name__)


class VirusTotalPlugin(Plugin):
    @property
    def enabled(self):
        return settings.VIRUSTOTAL_API_KEY is not None

    def activate(self):
        self.service = VirusTotal(settings.VIRUSTOTAL_API_KEY)


class VirusTotalIPReputationPlugin(IPExtractor, VirusTotalPlugin):
    def report(self, message, active=True):
        reports = self.retrieve_reports()
        if not reports:
            message.react('fog')
            if active:
                message.reply('No VirusTotal IP reputation reports for %s' %
                              ', '.join(self.ips))
            return
        for report in reports:
            if active:
                message.reply(self.format_report(report))
            else:
                message.send(self.format_report(report))

    def retrieve_reports(self):
        reports = []
        for ip in self.ips:
            try:
                reports.append(self.service.ip(ip))
            except Exception as e:
                logger.debug('Error retrieving IP reputation for %s: %s' % (
                    ip, e.message))
                break
        return reports

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
        return ' '.join(result)



