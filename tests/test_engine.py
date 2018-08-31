from unittest import main

from opyncorporates import create_engine
from .base import BaseTestCase


class TestEngine(BaseTestCase):

    def setUp(self):
        super(TestEngine, self).setUp()
        self.engine = create_engine(api_version=self.api_version, api_token=self.api_token)

    def tearDown(self):
        super(TestEngine, self).tearDown()
        self.engine = None

    def test_config(self):
        self.assertEqual(self.engine.api_token, self.api_token)
        self.assertEqual(self.engine.api_version, self.api_version)

    def test_search(self):
        search = self.engine.search('companies', q='Kellog')
        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['companies', 'search'])
        self.assertEqual(search.vars['q'], 'kellog')

    def test_search_with_invalid_search_type(self):
        self.assertRaises(NotImplementedError, self.engine.search, 'test', q='Kellog')

    def test_search_with_missing_q(self):
        self.assertRaises(ValueError, self.engine.search, 'companies')

    def test_search_company(self):
        search = self.engine.search_company(q='Kellog')
        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['companies', 'search'])
        self.assertEqual(search.vars['q'], 'kellog')

    def test_search_company_with_missing_q(self):
        self.assertRaises(TypeError, self.engine.search_company)

    def test_search_officer(self):
        search = self.engine.search_officer('Elon Musk')
        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['officers', 'search'])
        self.assertEqual(search.vars['q'], 'elon+musk')

    def test_search_officer_with_missing_q(self):
        self.assertRaises(TypeError, self.engine.search_officer)

    def test_fetch(self):
        fetch = self.engine.fetch(self.api_version, 'companies', 'gb',
                                  '00102498', api_token=self.api_token)


if __name__ == '__main__':
    main()