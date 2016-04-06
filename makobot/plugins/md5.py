import re

from slackbot.bot import listen_to, respond_to

MD5_REGEX = re.compile(r'([a-fA-F\d]{32})')


def extract_md5s(message):
    return set(MD5_REGEX.findall(message.body.get('text', '')))


@respond_to(MD5_REGEX)
def md5_active(message):
    message.reply('I will provide info about this md5')


@listen_to(MD5_REGEX)
def md5_passive(message):
    message.send('I will provide info about this md5')
