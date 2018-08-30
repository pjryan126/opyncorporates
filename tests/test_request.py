from unittest import main, TestCase

from opyncorporates import Request

import yaml

# get config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)['opyncorporates']

class TestRequest(TestCase):

    def setUp(self):
        self.api_token = cfg.get('api_token', None)
        self.api_version = cfg.get('api_version', '0.4')
        self.url = f"https://api.opencorporates.com/" \
                   f"v0.4/companies/search?" \
                   f"q=kellog&api_token={self.api_token}"

    def test_build_from_url(self):
        """ Test __build_from_url method."""
        url = 'https://api.opencorporates.com/v0.4/companies/search?q=kellog'
        request = Request(url, api_token=self.api_token)
        self.assertEqual(request.url, self.url)
        self.assertEqual(request.args, ['companies', 'search'])
        self.assertEqual(request.vars, {'q': 'kellog', 'api_token': self.api_token})

    def test_build_from_route(self):
        route = '/companies/search?q=kellog'
        request = Request(route, api_token=self.api_token)
        self.assertEqual(request.url, self.url)

    def test_build(self):
        request = Request(self.api_version, 'companies', 'search',
                          q='Kellog', api_token=self.api_token)
        self.assertEqual(request.url, self.url)