import re
from urlparse import urlparse

from slackbot.bot import listen_to, respond_to

from makobot import slackbot_settings as settings
from makobot.libs.xforce import XForce

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
            urlrs.append(xforce.url(url))
        except Exception:
            pass
    return urlrs


def urlr_report(urlr, inline=False):
    """REturns a URL reputation report"""
    report = []
    if 'result' not in urlr:
        return report
    urlr = urlr['result']
    if 'url' in urlr:
        report.append('X-Force URL Reputation for %s' % urlr['url'])
    if 'score' in urlr:
        report.append('Score: %s' % urlr['score'])
        report.append('Risk Level: %s' % XForce.risk_level(urlr['score']))
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
    urls = extract_urls(message)
    print('Found: %s' % ', '.join(urls))
    urlrs = xforce_url(urls)
    if not urlrs:
        message.reply('No reputation reports for %s' % ', '.join(urls))
    for urlr in urlrs:
        message.reply(urlr_report(urlr))


@listen_to(URL_REGEX)
def url_passive(message, *args):
    urls = extract_urls(message)
    urlrs = xforce_url(urls)
    react = False
    for urlr in urlrs:
        if urlr.get('result', {}).get('score', 0) >= 3:
            message.send(urlr_report(urlr, inline=True))
            react = True
    if react:
        message.react('warning')
