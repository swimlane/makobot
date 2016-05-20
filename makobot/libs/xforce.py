# -*- coding: utf-8 -*-

import requests


class XForce(object):
    def __init__(self, api_key, api_password):
        self.base_url = 'https://api.xforce.ibmcloud.com'
        self.session = requests.Session()
        self.session.auth = (api_key, api_password)

    def get(self, *uri, **params):
        r = self.session.get('/'.join([self.base_url] + list(uri)),
                             params=params)
        r.raise_for_status()
        return r.json()

    def host(self, host):
        return self.get('whois', host)

    def ip(self, ip):
        return self.get('ipr', ip)

    def md5(self, md5):
        return self.get('malware', md5)

    def url(self, url):
        return self.get('url', url)
