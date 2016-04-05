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

    def ipr(self, ip):
        return self.get('ipr', ip)

    def url(self, url):
        return self.get('url', url)

    @classmethod
    def risk_level(cls, score):
        if score < 2:
            return 'VERY LOW'
        elif 2 <= score < 3:
            return 'LOW'
        elif 3 <= score < 5:
            return 'MODERATE'
        elif 5 <= score < 8:
            return 'HIGH'
        elif score >= 8:
            return 'VERY HIGH'
        return 'UNKNOWN'
