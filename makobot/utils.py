# -*- coding: utf-8 -*-

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def clean_url(url):
    """Returns only the scheme and domain of URL, minus Slack formatting"""
    url = url.lstrip('<').rstrip('>')
    parsed_url = urlparse(url)
    return '{url.scheme}://{url.netloc}'.format(url=parsed_url)


def host_only(url):
    """Returns only the host of URL, minus Slack formatting"""
    url = url.lstrip('<').rstrip('>')
    host = urlparse(url).netloc
    if '@' in host:
        host = host.split('@')[-1]
    if ':' in host:
        host = host.split(':')[0]
    return host


def reaction_to_int(reaction):
    reaction_map = {
        'fog': 0,
        'sunny': 1,
        'mostly_sunny': 2,
        'partly_sunny': 3,
        'barely_sunny': 4,
        'cloud': 5,
        'rain_cloud': 6,
        'thunder_cloud_and_rain': 7,
        'lightning': 8,
        'tornado': 9}
    return reaction_map.get(reaction, 0)
