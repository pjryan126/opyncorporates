from unittest import main

from opyncorporates import FetchRequest
from .base import BaseTestCase


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


if __name__ == '__main__':
    main()