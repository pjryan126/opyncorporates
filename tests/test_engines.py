from unittest import main

from opyncorporates import create_engine
from tests.base import BaseTestCase


class TestEngineV04(BaseTestCase):

    def setUp(self):
        super(TestEngineV04, self).setUp()
        self.engine = create_engine(api_version=self.api_version, api_token=self.api_token)

    def tearDown(self):
        super(TestEngineV04, self).tearDown()
        self.engine = None

    def test_config(self):
        self.assertEqual(self.engine.api_token, self.api_token)
        self.assertEqual(self.engine.api_version, self.api_version)

    def test_search(self):

        search = self.engine.search('companies', q='Kellog')

        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['companies', 'search'])
        self.assertEqual(search.vars['q'], 'kellog')
        self.assertEqual(search.response.status_code, 200)

    def test_search_with_invalid_search_type(self):
        self.assertRaises(NotImplementedError, self.engine.search, 'test', q='Kellog')

    def test_search_with_missing_q(self):
        self.assertRaises(ValueError, self.engine.search, 'companies')

    def test_fetch(self):
        fetch = self.engine.fetch('companies', 'gb', '00102498')
        self.assertEqual(fetch.results['name'], "BP P.L.C.")

    def test_fetch_with_bad_identifier(self):
        bad_fetch = self.engine.fetch('companies', 'gb', '1')
        self.assertEqual(bad_fetch.response.status_code, 404)
        self.assertEqual(bad_fetch.results, None)