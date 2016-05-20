# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to

from makobot.plugins.extractor import MD5Extractor
from makobot.plugins.manager import plugin_manager


@respond_to(MD5Extractor.REGEX)
def md5_active(message, *args):
    """
    Actively respond to direct messages with malware reports. The active
    version of this bot is meant to be more of a query service.
    """
    plugin_manager.evaluate('md5', message)


@listen_to(MD5Extractor.REGEX)
def md5_passive(message, *args):
    """
    Passively monitor channels and report malware when found. The passive
    version of this bot is meant to be a monitoring service.
    """
    plugin_manager.evaluate('md5', message, False)
