# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to

from makobot.plugins.extractor import IPExtractor
from makobot.plugins.manager import plugin_manager


@respond_to(IPExtractor.REGEX)
def ip_active(message, *args):
    """
    Respond to direct messages with an IP reputation report. The active
    version of this bot is meant to be a query service.
    """
    plugin_manager.evaluate('ip', message)


@listen_to(IPExtractor.REGEX)
def ip_passive(message, *args):
    """
    Monitor channels and report IP reputations above a certain threshold. This
    version of the bot is meant to be a monitoring service.
    """
    plugin_manager.evaluate('ip', message, False)
