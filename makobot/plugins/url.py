# -*- coding: utf-8 -*-

import re
from urlparse import urlparse

from slackbot.bot import listen_to, respond_to

from .. import slackbot_settings as settings
from ..libs.xforce import XForce
from ..utils import reaction, risk_level

URL_REGEX = re.compile(r'(?:https?://[^\s]+)')


def extract_urls(message):
    """REturns the URLs contained within the message text"""
    return set([clean_url(url)
                for url in URL_REGEX.findall(message.body.get('text', ''))])


def clean_url(url):
    """Returns only the scheme and domain of URL, minus Slack formatting"""
    url = url.lstrip('<').rstrip('>')
    parsed_url = urlparse(url)
    return '{url.scheme}://{url.netloc}'.format(url=parsed_url)


def xforce_url(urls):
    """Returns the URL reputations for the provided URLs from IBM x-Force"""
    urlrs = []
    if not settings.XFORCE_API_KEY or not settings.XFORCE_PASSWORD:
        return urlrs
    xforce = XForce(settings.XFORCE_API_KEY, settings.XFORCE_PASSWORD)
    for url in urls:
        try:
            urlr = xforce.url(url)
            if 'result' in urlr:
                urlrs.append(urlr['result'])
        except Exception:
            pass
    return urlrs


def urlr_report(urlr, inline=False):
    """REturns a URL reputation report"""
    report = []
    if 'url' in urlr:
        report.append('X-Force URL Reputation for %s' % urlr['url'])
    if 'score' in urlr:
        report.append('Score: %s' % urlr['score'])
        report.append('Risk Level: %s' % risk_level(urlr['score']))
    if 'reason' in urlr:
        report.append('Reason: %s' % urlr['reason'])
    if 'cats' in urlr and urlr['cats']:
        report.append('Categories: %s' % ', '.join([
            k for k, v in urlr['cats'].items()]))
    if inline:
        return ' '.join(report)
    return '\n'.join(report)


@respond_to(URL_REGEX)
def url_active(message, *args):
    """
    Responds to direct messages with a URL reputation report. The active
    version of this bot is meant to be a query service.
    """
    urls = extract_urls(message)
    urlrs = xforce_url(urls)

    if not urlrs:
        message.react('fog')
        message.reply('No URL reputation reports for %s' % ', '.join(urls))
        return

    high_score = 1
    for urlr in urlrs:
        message.reply(urlr_report(urlr))
        if 'score' in urlr and urlr['score'] > high_score:
            high_score = urlr['score']
    message.react(reaction(high_score))


@listen_to(URL_REGEX)
def url_passive(message, *args):
    """
    Monitor channels and report URL reputations above a certain threshold.
    This version of the bot is meant to be a monitoring service.
    """
    urls = extract_urls(message)
    urlrs = xforce_url(urls)

    if not urlrs:
        message.react('fog')
        return

    high_score = 1
    for urlr in urlrs:
        if 'score' in urlr:
            if urlr['score'] >= 3:
                message.send(urlr_report(urlr, inline=True))
            if urlr > high_score:
                high_score = urlr['score']
    message.react(reaction(high_score))
