import logging

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
                'ThreatConnect client must be installed: '
                'pip install threatconnect')
        self.service = ThreatConnect(
            settings.THREATCONNECT_ACCESS_ID,
            settings.THREATCONNECT_SECRET_KEY,
            settings.THREATCONNECT_DEFAULT_ORG)
        self.service.set_api_result_limit(100)

    def retrieve_indicators(self, indicator):
        indicators = self.service.indicators()
        f = indicators.add_filter()
        f.add_owner(['Common Community'])
        f.add_indicator(indicator)
        return indicators.retrieve()


class ThreatConnectEmailPlugin(EmailExtractor, ThreatConnectPlugin):
    pass


# Register Plugins
plugin_manager.register('email', ThreatConnectEmailPlugin)
