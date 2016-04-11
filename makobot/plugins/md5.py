# -*- coding: utf-8 -*-

import re

from slackbot.bot import listen_to, respond_to

from .. import slackbot_settings as settings
from ..libs.xforce import XForce

MD5_REGEX = re.compile(r'([a-fA-F\d]{32})')


def extract_md5s(message):
    """Returns all the MD5 checksums found in a message"""
    return set(MD5_REGEX.findall(message.body.get('text', '')))


def xforce_malware(md5s):
    """Returns information about malware matching the MD5"""
    md5rs = []
    if not settings.XFORCE_API_KEY or not settings.XFORCE_PASSWORD:
        return md5rs
    xforce = XForce(settings.XFORCE_API_KEY, settings.XFORCE_PASSWORD)
    for md5 in md5s:
        try:
            md5rs.append(xforce.malware(md5))
        except Exception:
            pass
    return md5rs


def md5r_report(md5r, inline=False):
    """REturns a malware report"""
    report = []
    if 'md5' in md5r:
        report.append('X-Force Malware Report for %s' % md5r['md5'])
    if 'family' in md5r:
        report.append('Malware Family: %s' % ', '.join(md5r['family']))
    if 'risk' in md5r:
        report.append('Risk: %s' % md5r['risk'])
    if inline:
        return ' '.join(report)
    return '\n'.join(report)


@respond_to(MD5_REGEX)
def md5_active(message):
    """
    Actively respond to direct messages with malware reports. The active
    version of this bot is meant to be more of a query service.
    """
    md5s = extract_md5s(message)
    md5rs = xforce_malware(md5s)
    if not md5rs:
        message.reaction('fog')
        message.reply('No malware reports for %s' % ', '.join(md5s))
        return
    for md5r in md5rs:
        message.reply(md5r_report(md5r))
        message.reaction('lightning')


@listen_to(MD5_REGEX)
def md5_passive(message):
    """
    Passively monitor channels and report malware when found. The passive
    version of this bot is meant to be a monitoring service.
    """
    md5s = extract_md5s(message)
    md5rs = xforce_malware(md5s)
    for md5r in md5rs:
        message.reply(md5r_report(md5r))
        message.reaction('lightning')
