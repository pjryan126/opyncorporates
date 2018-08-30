from unittest import main, TestCase

from opyncorporates import FetchRequest

import yaml

# get config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)['opyncorporates']


class TestFetchRequest(TestCase):

    def setUp(self):
        self.api_token = cfg.get('api_token', None)
        self.api_version = cfg.get('api_version', '0.4')
        self.fetch = FetchRequest(self.api_version, 'companies','gb', '00102498',
                                  api_token=self.api_token)
        self.test_url = f"https://api.opencorporates.com/v{self.api_version}/" \
                        f"companies/gb/00102498?api_token={self.api_token}"

    def tearDown(self):
        self.api_token = None
        self.api_version = None
        self.fetch = None
        self.test_url = None

    def test_fetch_request(self):
        """ Test FetchRequest instantation."""
        self.assertEqual(self.fetch.url, self.test_url)