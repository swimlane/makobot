import re

from slackbot.bot import listen_to, respond_to

from makobot import slackbot_settings as settings
from makobot.libs.xforce import XForce

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
        report.append('Risk Level: %s' % XForce.risk_level(ipr['score']))
    if 'reason' in ipr:
        report.append('Reason: %s' % ipr['reason'])
    if 'cats' in ipr and ipr['cats']:
        report.append('Categories: %s' % ', '.join([
            '%s (%s)' % (k, v) for k, v in ipr['cats'].items()]))
    if inline:
        return ' '.j(report)
    return '\n'.join(report)


@respond_to(IP_REGEX)
def ip_active(message):
    ips = extract_ips(message)
    iprs = xforce_ipr(ips)
    if not iprs:
        message.reply('No reputation reports for %s' % ', '.join(iprs))
    for ipr in iprs:
        message.reply(ipr_report(ipr))


@listen_to(IP_REGEX)
def ip_passive(message):
    ips = extract_ips(message)
    iprs = xforce_ipr(ips)
    react = False
    for ipr in iprs:
        if 'score' in ipr and ipr['score'] >= 3:
            message.send(ipr_report(ipr, inline=True))
            react = True
    if react:
        message.react('warning')
