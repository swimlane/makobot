from __future__ import absolute_import

import logging

try:
    from threatconnect.Config.IndicatorType import IndicatorType
except ImportError:
    IndicatorType = None

from makobot import slackbot_settings as settings

from .base import Plugin
from .extractor import EmailExtractor
from .manager import plugin_manager

logger = logging.getLogger(__name__)


class ThreatConnectPlugin(Plugin):
    @property
    def enabled(self):
        return settings.THREATCONNECT_ACCESS_ID is not None and \
            settings.THREATCONNECT_SECRET_KEY is not None and \
            settings.THREATCONNECT_DEFAULT_ORG is not None

    def activate(self):
        try:
            from threatconnect import ThreatConnect  # noqa
        except ImportError:
            raise ImportError(
                'ThreatConnect client must be installed to use this plugin: '
                'pip install threatconnect')
        self.service = ThreatConnect(
            settings.THREATCONNECT_ACCESS_ID,
            settings.THREATCONNECT_SECRET_KEY,
            settings.THREATCONNECT_DEFAULT_ORG,
            settings.THREATCONNECT_BASE_URL)
        self.service.set_api_result_limit(100)

    def retrieve_indicator(self, indicator, indicator_type=None):
        indicators = self.service.indicators()
        if indicator_type:
            f = indicators.add_filter(indicator_type)
        else:
            f = indicators.add_filter()
        f.add_owner(['Common Community'])
        f.add_indicator(indicator)
        results = sorted(indicators.retrieve(), key=lambda x: x.confidence)
        return results[-1]

    def threshold_met(self, report):
        return hasattr(report, 'rating') and report.rating >= 1 and \
            hasattr(report, 'confidence') and report.confidence >= 50

    def react(self, message):
        if not any(self.reports.values()):
            message.react('fog')
            return
        rating = max([r.rating for r in self.reports.values() if r.rating])
        message.react(self.reaction(rating))

    def reaction(self, score):
        if score == 0:
            return 'sunny'
        elif 0 <= score < 0.5:
            return 'mostly_sunny'
        elif 0.5 <= score < 1:
            return 'partly_sunny'
        elif 1 <= score < 2:
            return 'barely_sunny'
        elif 2 <= score < 2.5:
            return 'cloud'
        elif 2.5 <= score < 3:
            return 'rain_cloud'
        elif 3 <= score < 3.5:
            return 'thunder_cloud_and_rain'
        elif 3.5 <= score < 4:
            return 'lightning'
        elif score >= 4:
            return 'tornado'

    def risk_level(self, score):
        try:
            score = float(score)
        except TypeError:
            return 'UNKNOWN'

        if score == 0:
            return 'UNKNOWN'
        elif 0 < score < 1:
            return 'VERY LOW'
        elif 1 <= score < 2:
            return 'LOW'
        elif 2 <= score < 3:
            return 'MODERATE'
        elif 3 <= score < 4:
            return 'HIGH'
        elif score >= 4:
            return 'VERY HIGH'


class ThreatConnectEmailPlugin(EmailExtractor, ThreatConnectPlugin):
    def retrieve(self):
        for email in self.reports:
            try:
                report = self.retrieve_indicator(
                    email, IndicatorType.EMAIL_ADDRESSES)
            except Exception as e:
                logger.debug('Error retrieving email report for %s: %s' % (
                    email, e.message))
                continue
            if report:
                self.reports[email] = report

    def format(self, subject, report):
        result = []
        result.append('ThreatConnect email report for %s' % subject)
        if report.description:
            result.append('Description: %s' % report.description)
        if report.rating:
            result.append('Rating: %s' % report.rating)
            result.append('Risk Level: %s' %
                          self.risk_level(report.rating))
        if report.confidence:
            result.append('Confidence: %s' % report.confidence)
        return ' '.join(result)


# Register Plugins
plugin_manager.register('email', ThreatConnectEmailPlugin)