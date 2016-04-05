import re

from slackbot.bot import listen_to, respond_to

URL_REGEX = re.compile(r'(https?://[^\s]+)')


@respond_to(URL_REGEX)
def url_active(message):
    pass


@listen_to(URL_REGEX)
def url_passive(message):
    pass
