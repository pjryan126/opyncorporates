from unittest import main

from opyncorporates import FetchRequest, Request, SearchRequest
from .base import BaseTestCase


class TestRequest(BaseTestCase):

    def setUp(self):
        super(TestRequest, self).setUp()
        self.url = "https://api.opencorporates.com/" \
                   "v0.4/companies/search?" \
                   "q=kellog&api_token=%s" % self.api_token

    def tearDown(self):
        super(TestRequest, self).tearDown()
        self.url = None

    def test_build_from_url(self):
        """ Test __build_from_url method."""
        url = 'https://api.opencorporates.com/v0.4/companies/search?q=kellog'
        request = Request(url, api_token=self.api_token)
        self.assertEqual(request.url, self.url)
        self.assertEqual(request.args, ['companies', 'search'])
        self.assertEqual(request.vars, {'q': 'kellog', 'api_token': self.api_token})

    def test_build_from_route(self):
        route = 'v%s/companies/search?q=kellog' % self.api_version
        request = Request(route, api_token=self.api_token)
        self.assertEqual(request.url, self.url)

    def test_build(self):
        request = Request(self.api_version, 'companies', 'search',
                          q='Kellog', api_token=self.api_token)
        self.assertEqual(request.url, self.url)


class TestFetchRequest(BaseTestCase):

    def setUp(self):

        super(TestFetchRequest, self).setUp()

        self.jurisdiction = 'gb'
        self.company_id = '00102498'

        self.fetch = FetchRequest(self.api_version, 'companies',
                                  self.jurisdiction, self.company_id,
                                  api_token=self.api_token)

        self.test_url = "https://api.opencorporates.com/v%s/companies/%s/%s?" \
                        "api_token=%s" % (self.api_version, self.jurisdiction,
                                          self.company_id, self.api_token)

    def tearDown(self):
        super(TestFetchRequest, self).tearDown()
        self.fetch = None
        self.test_url = None

    def test_valid_fetch_request(self):
        """ "Test results of valid fetch """
        self.assertEqual(type(self.fetch.results), dict)
        self.assertEqual(self.fetch.url, self.test_url)
        self.assertEqual(self.fetch.results['name'], "BP P.L.C.")

    def test_invalid_fetch_request(self):

        bad_fetch = FetchRequest(self.api_version, 'companies',
                                 self.jurisdiction, '00101498',
                                 api_token=self.api_token)

        self.assertEqual(bad_fetch.response.status_code, 404)
        self.assertEqual(bad_fetch.results, None)


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