from unittest import main, TestCase

from opyncorporates import SearchRequest

import yaml

# get config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)['opyncorporates']


class TestSearchRequest(TestCase):

    def setUp(self):
        self.api_token = cfg.get('api_token', None)
        self.api_version = cfg.get('api_version', '0.4')
        self.search = SearchRequest(self.api_version, 'companies', q='Kellog',
                                    api_token=self.api_token)

    def tearDown(self):
        self.api_token = None
        self.api_version = None
        self.search = None

    def test_search_request(self):
        """ Test SearchRequest instantation."""
        self.assertEqual(self.search.total_pages, len(self.search.page_urls))
        self.assertEqual(self.search.per_page, 30)

    def test_results(self):
        """ Test SearchRequest.results property."""
        count = 0
        for r in self.search.results:
            count += 1
        self.assertEqual(self.search.total_count, count)

    def test_get_page(self):
        """ Test SearchRequest.get_page method."""
        page_results = self.search.get_page(1)
        self.assertEqual(len(page_results), 30)


