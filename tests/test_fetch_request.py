from unittest import main

from opyncorporates import FetchRequest
from .base import BaseTestCase


class TestFetchRequest(BaseTestCase):

    def setUp(self):
        super(TestFetchRequest, self).setUp()
        id = '00102498'
        self.fetch = FetchRequest(self.api_version, 'companies','gb', id,
                                  api_token=self.api_token)
        self.test_url = "https://api.opencorporates.com/v%s/companies/gb/%s?" \
                        "api_token=%s" % (self.api_version, id, self.api_token)

    def tearDown(self):
        super(TestFetchRequest, self).tearDown()
        self.fetch = None
        self.test_url = None

    def test_fetch_request(self):
        """ Test FetchRequest instantation."""
        self.assertEqual(self.fetch.url, self.test_url)

if __name__ == '__main__':
    main()