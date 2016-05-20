# -*- coding: utf-8 -*-

from requests import Session


class VirusTotal(object):
    def __init__(self, api_key):
        self.base_url = 'https://www.virustotal.com/vtapi/v2'
        self.session = Session()
        self.api_key = api_key

    def get(self, *uri, **params):
        params.update(apikey=self.api_key)
        r = self.session.get('/'.join([self.base_url] + list(uri)),
                             params=params)
        r.raise_for_status()
        return r.json()

    def host(self, host):
        return self.get('domain', 'report', domain=host)

    def ip(self, ip):
        return self.get('ip-address', 'report', ip=ip)

    def md5(self, md5):
        return self.get('file', 'report', resource=md5, allinfo=1)

    def url(self, url):
        return self.get('url', 'report', resource=url, scan=1)
