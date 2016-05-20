# -*- coding: utf-8 -*-

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from slackbot.bot import Bot  # noqa

from . import slackbot_settings as settings  # noqa

assert settings.API_TOKEN, 'SLACK_TOKEN environment variable must be set'

makobot_logger = logging.getLogger('makobot')
makobot_logger.addHandler(logging.StreamHandler())
makobot_logger.setLevel(logging.INFO)
if settings.DEBUG:
    makobot_logger.setLevel(logging.DEBUG)

slackbot_logger = logging.getLogger('slackbot')
slackbot_logger.addHandler(logging.StreamHandler())
slackbot_logger.setLevel(logging.INFO)
if settings.DEBUG:
    slackbot_logger.setLevel(logging.DEBUG)

Bot().run()
