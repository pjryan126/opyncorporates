from unittest import main, TestCase

from opyncorporates import create_engine

import yaml

# get config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)['opyncorporates']


class TestEngine(TestCase):

    def setUp(self):
        self.api_token = cfg.get('api_token', None)
        self.api_version = cfg.get('api_version', '0.4')
        self.engine = create_engine(api_version=self.api_version, api_token=self.api_token)

    def tearDown(self):
        self.api_token = None
        self.api_version = None
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
        self.assertRaises(ValueError, self.engine.search, 'test', q='Kellog')

    def test_search_with_missing_q(self):
        self.assertRaises(ValueError, self.engine.search, 'test')

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


if __name__ == '__main__':
    main()