import re

from slackbot.bot import listen_to, respond_to

IP_REGEX = re.compile(
    r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})')


@respond_to(IP_REGEX)
def ip_active(message):
    pass


@listen_to(IP_REGEX)
def ip_passive(message):
    pass
