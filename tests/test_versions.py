from unittest import main

from opyncorporates import create_engine
from .base import BaseTestCase


class TestVersion(BaseTestCase):
    """ Test Version Class using default v0.4 configuration. """

    def setUp(self):

        super(TestVersion, self).setUp()
        self.engine = create_engine(api_version=self.api_version, api_token=self.api_token)

    def tearDown(self):

        super(TestVersion, self).tearDown()
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

    def test_fetch(self):
        fetch = self.engine.fetch('companies', 'gb', '00102498')
        self.assertEqual(fetch.results['name'], "BP P.L.C.")

    def test_search_with_invalid_search_type(self):

        self.assertRaises(NotImplementedError, self.engine.search, 'test', q='Kellog')

    def test_search_with_missing_q(self):

        self.assertRaises(ValueError, self.engine.search, 'companies')

    def test_search_company(self):

        search = self.engine.search_company(q='Kellog')

        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['companies', 'search'])
        self.assertEqual(search.vars['q'], 'kellog')
        self.assertEqual(search.response.status_code, 200)

    def test_search_company_with_missing_q(self):

        self.assertRaises(TypeError, self.engine.search_company)

    def test_fetch_company(self):

        self.country_code = 'gb'
        self.company_id = '00102498'

        fetch = self.engine.fetch_company(self.country_code, self.company_id)
        self.assertEqual(fetch.response.status_code, 200)
        self.assertEqual(fetch.results['name'], "BP P.L.C.")

    def test_fetch_invalid_company(self):

        self.country_code = 'gb'
        self.company_id = '00101498'

        fetch = self.engine.fetch_company(self.country_code, self.company_id)

        self.assertEqual(fetch.response.status_code, 404)
        self.assertEqual(fetch.results, None)

    def test_search_officer(self):

        search = self.engine.search_officer('Elon Musk')

        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['officers', 'search'])
        self.assertEqual(search.vars['q'], 'elon+musk')
        self.assertEqual(search.response.status_code, 200)

    def test_search_officer_with_missing_q(self):

        self.assertRaises(TypeError, self.engine.search_officer)

    def test_fetch_officer(self):

        officer_id = '163522168'
        fetch = self.engine.fetch_officer(officer_id)

        self.assertEqual(fetch.response.status_code, 200)
        self.assertEqual(str(fetch.results['id']), officer_id)

    def test_fetch_invalid_officer(self):

        officer_id = 'abc'
        fetch = self.engine.fetch_officer(officer_id)

        self.assertEqual(fetch.response.status_code, 404)
        self.assertEqual(fetch.results, None)

    def test_search_corporate_groupings(self):

        search = self.engine.search_corporate_groupings('bar')

        self.assertEqual(search.api_version, '0.4')
        self.assertEqual(search.args, ['corporate_groupings', 'search'])
        self.assertEqual(search.vars['q'], 'bar')
        self.assertEqual(search.response.status_code, 200)

    def test_search_corporate_groupings_with_missing_q(self):
        self.assertRaises(TypeError, self.engine.search_officer)

    def test_fetch_corporate_groupings(self):

        fetch = self.engine.fetch_corporate_groupings('capita')

        self.assertEqual(fetch.response.status_code, 200)
        self.assertEqual(fetch.results['name'], 'capita')

    def test_fetch_filing(self):

        filing_id = '1'
        fetch = self.engine.fetch_filing(filing_id)

        self.assertEqual(fetch.response.status_code, 200)
        self.assertEqual(str(fetch.results['id']), filing_id)

    def test_fetch_data(self):

        self.assertRaises(NotImplementedError, self.engine.fetch_data, 'test')

    def test_search_gazette_notices(self):

        search = self.engine.search_gazette_notices('bar')

        self.assertEqual(search.args, ['statements', 'gazette_notices', 'search'])
        self.assertEqual(search.vars['q'], 'bar')
        self.assertEqual(search.response.status_code, 200)

    def test_search_control_statements(self):

        search = self.engine.search_control_statements('bar')

        self.assertEqual(search.args, ['statements', 'control_statements', 'search'])
        self.assertEqual(search.vars['q'], 'bar')
        self.assertEqual(search.response.status_code, 200)

    def test_fetch_statement(self):

        statement_id = '11499887'
        fetch = self.engine.fetch_statement(statement_id)

        self.assertEqual(fetch.response.status_code, 200)
        self.assertEqual(str(fetch.results['id']), statement_id)

    def test_fetch_placeholder(self):
        placeholder_id = '1'
        fetch = self.engine.fetch_placeholder(placeholder_id)

        self.assertEqual(fetch.response.status_code, 200)
        self.assertEqual(str(fetch.results['id']), placeholder_id)
        self.assertFalse(len(fetch.network) > 0)

    def test_fetch_jurisdictions(self):

        fetch = self.engine.fetch_jurisdictions()

        self.assertEqual(fetch.response.status_code, 200)
        self.assertNotEqual(fetch.results, [])

if __name__ == '__main__':
    main()