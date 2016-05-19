# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to

from makobot.plugins.extractor import HostExtractor
from makobot.plugins.manager import plugin_manager


@respond_to(HostExtractor.REGEX)
def host_active(message, *args):
    """
    Responds to direct messages with a host reputation report. The active
    version of this bot is meant to be a query service.
    """
    plugin_manager.evaluate('host', message)


@listen_to(HostExtractor.REGEX)
def host_passive(message, *args):
    """
    Monitor channels and report host reputations above a certain threshold.
    This version of the bot is meant to be a monitoring service.
    """
    plugin_manager.evaluate('host', message, False)
