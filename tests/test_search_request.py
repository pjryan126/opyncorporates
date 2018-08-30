from unittest import main

from opyncorporates import SearchRequest
from .base import BaseTestCase


class TestSearchRequest(BaseTestCase):

    def setUp(self):
        super(TestSearchRequest, self).setUp()
        self.search = SearchRequest(self.api_version, 'companies', q='Kellog',
                                    api_token=self.api_token)

    def tearDown(self):
        super(TestSearchRequest, self).tearDown()
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

if __name__ == '__main__':
    main()

