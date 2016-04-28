# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to

from makobot.plugins.extractor import URLExtractor
from makobot.plugins.manager import plugin_manager


@respond_to(URLExtractor.REGEX)
def url_active(message, *args):
    """
    Responds to direct messages with a URL reputation report. The active
    version of this bot is meant to be a query service.
    """
    plugin_manager.evaluate('url', message)


@listen_to(URLExtractor.REGEX)
def url_passive(message, *args):
    """
    Monitor channels and report URL reputations above a certain threshold.
    This version of the bot is meant to be a monitoring service.
    """
    plugin_manager.evaluate('url', message, False)
