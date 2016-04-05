import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from slackbot.bot import Bot

logger = logging.getLogger('slackbot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

Bot().run()
