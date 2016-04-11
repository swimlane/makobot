# -*- coding: utf-8 -*-

import re

from slackbot.bot import listen_to, respond_to

from .. import slackbot_settings as settings
from ..libs.xforce import XForce
from ..utils import reaction, risk_level

IP_REGEX = re.compile(
    r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})')


def extract_ips(message):
    """REturns the IPs contained within the message text"""
    return set(IP_REGEX.findall(message.body.get('text', '')))


def xforce_ipr(ips):
    """Returns the IP reputations for the provided IPs from IBM x-Force"""
    iprs = []
    if not settings.XFORCE_API_KEY or not settings.XFORCE_PASSWORD:
        return iprs
    xforce = XForce(settings.XFORCE_API_KEY, settings.XFORCE_PASSWORD)
    for ip in ips:
        try:
            iprs.append(xforce.ipr(ip))
        except Exception:
            pass
    return iprs


def ipr_report(ipr, inline=False):
    """REturns an IP reputation report"""
    report = []
    if 'ip' in ipr:
        report.append('X-Force IP Reputation for %s' % ipr['ip'])
    if 'score' in ipr:
        report.append('Score: %s' % ipr['score'])
        report.append('Risk Level: %s' % risk_level(ipr['score']))
    if 'reason' in ipr:
        report.append('Reason: %s' % ipr['reason'])
    if 'cats' in ipr and ipr['cats']:
        report.append('Categories: %s' % ', '.join([
            '%s (%s)' % (k, v) for k, v in ipr['cats'].items()]))
    if inline:
        return ' '.join(report)
    return '\n'.join(report)


@respond_to(IP_REGEX)
def ip_active(message):
    """Respond to direct messages with an IP reputation report. The active
    version of this bot is meant to be a query service.
    """
    ips = extract_ips(message)
    iprs = xforce_ipr(ips)

    if not iprs:
        message.reaction('fog')
        message.reply('No IP reputation reports for %s' % ', '.join(ips))
        return

    high_score = 1
    for ipr in iprs:
        message.reply(ipr_report(ipr))
        if 'score' in ipr and ipr['score'] > high_score:
            high_score = ipr['score']
    message.reaction(reaction(high_score))


@listen_to(IP_REGEX)
def ip_passive(message):
    """
    Monitor channels and report IP reputations above a certain threshold. This
    version of the bot is meant to be a monitoring service.
    """
    ips = extract_ips(message)
    iprs = xforce_ipr(ips)

    if not iprs:
        message.react('fog')
        return

    high_score = 1
    for ipr in iprs:
        if 'score' in ipr:
            if ipr['score'] >= 3:
                message.send(ipr_report(ipr, inline=True))
            if ipr['score'] > high_score:
                high_score = ipr['score']
    message.react(reaction(high_score))
