from unittest import main

from opyncorporates import Request
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

if __name__ == '__main__':
    main()