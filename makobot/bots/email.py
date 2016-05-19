# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to

from makobot.plugins.extractor import EmailExtractor
from makobot.plugins.manager import plugin_manager


@respond_to(EmailExtractor.REGEX)
def email_active(message, *args):
    """
    Responds to direct messages with a email reputation report. The active
    version of this bot is meant to be a query service.
    """
    plugin_manager.evaluate('email', message)


@listen_to(EmailExtractor.REGEX)
def email_passive(message, *args):
    """
    Monitor channels and report email reputations above a certain threshold.
    This version of the bot is meant to be a monitoring service.
    """
    plugin_manager.evaluate('email', message, False)
