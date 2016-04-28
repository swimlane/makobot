from urlparse import urlparse


def clean_url(url):
    """Returns only the scheme and domain of URL, minus Slack formatting"""
    url = url.lstrip('<').rstrip('>')
    parsed_url = urlparse(url)
    return '{url.scheme}://{url.netloc}'.format(url=parsed_url)
