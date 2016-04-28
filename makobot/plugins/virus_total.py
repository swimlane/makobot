from makobot import slackbot_settings as settings
from makobot.libs.virustotal import VirusTotal

from .base import Plugin


class VirusTotalPlugin(Plugin):
    @property
    def enabled(self):
        return settings.VIRUSTOTAL_API_KEY is not None

    def activate(self):
        self.virustotal = VirusTotal(settings.VIRUSTOTAL_API_KEY)
