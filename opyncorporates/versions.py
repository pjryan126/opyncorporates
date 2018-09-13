import abc

from opyncorporates.api import (
    Request,
    FetchRequest,
    SearchRequest
)

"""Version strategies for creating new instances of Engine types.

These are semi-private implementation classes which provide the
underlying behavior for the "api_version" keyword argument available on
:func:`~opyncorporates.create_engine`.  The only current available 
option is ``0.4``.

New versions can be added via new ``Version`` classes.

"""

versions = {}


class VersionAbstract(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request(self):
        """Required Method"""

    @abc.abstractmethod
    def search(self, object_type, q=None, *args, **kwargs):
        """Required Method"""

    @abc.abstractmethod
    def search_company(self, q, **kwargs):
        """Required Method"""

    @abc.abstractmethod
    def search_officer(self, q, **kwargs):
        """Required Method"""

    @abc.abstractmethod
    def fetch(self, object_type, *args, **kwargs):
        """Required Method"""


class Version(VersionAbstract):

    def __init__(self, api_version, search_types, fetch_types,
                 match_types, api_token):

        self.api_version = api_version
        self.api_token = api_token
        self.search_types = search_types
        self.fetch_types = fetch_types
        self.match_types = match_types

        versions[self.api_version] = self.__class__

    def request(self, *args, **kwargs):
        return Request(*args, **kwargs)

    def search(self, search_type, *args, **kwargs):

        if search_type not in self.search_types:
            msg = "`%s` not available in v%s" % (search_type, self.api_version)
            raise NotImplementedError(msg)

        q = kwargs.pop('q', None)
        if q is None:
            msg = "Please provide a value for q as a keyword argument."
            raise ValueError(msg)

        # construct args
        args = list(args)
        args.insert(0, "v%s" % self.api_version)
        args.insert(1, search_type)

        # construct request_vars
        request_vars = dict()
        if self.api_token is not None:
            kwargs['api_token'] = self.api_token
        for k, v in kwargs.items():
            request_vars[k] = v

        return SearchRequest(*args, q=q, **request_vars)

    def fetch(self, fetch_type, *args, **kwargs):

        if fetch_type not in self.fetch_types:
            msg = "`%s` not available in v%s" % (fetch_type, self.api_version)
            raise NotImplementedError(msg)

        if len(args) == 0:
            msg = "Please provide an identifier value as a positional argument."
            raise ValueError(msg)

        # construct args
        args = list(args)
        args.insert(0, "v%s" % self.api_version)
        args.insert(1, fetch_type)

        # construct request_vars
        request_vars = dict()
        if self.api_token is not None:
            kwargs['api_token'] = self.api_token
        for k, v in kwargs.items():
            request_vars[k] = v

        return FetchRequest(fetch_type, *args, **request_vars)

    def search_company(self, q, **kwargs):
        return self.search('companies', q=q, **kwargs)

    def fetch_company(self, jurisdiction_code, identifier, **kwargs):
        return self.fetch('companies', jurisdiction_code, identifier, **kwargs)

    def search_officer(self, q, **kwargs):
        return self.search('officers', q=q, **kwargs)

    def fetch_officer(self, identifier, **kwargs):
        return self.fetch('officers', identifier, **kwargs)

    def search_corporate_groupings(self, q, **kwargs):
        return self.search('corporate_groupings', q=q, **kwargs)

    def fetch_corporate_groupings(self, identifier, **kwargs):
        return self.fetch('corporate_groupings', identifier, **kwargs)

    def fetch_filing(self, identifier, **kwargs):
        return self.fetch('filings', identifier, **kwargs)

    def fetch_data(self, identifier, **kwargs):
        msg = "The `data` type is being deprecated in favor of `statements`."
        raise NotImplementedError(msg)

    def search_gazette_notices(self, q, **kwargs):
        return self.search('statements', 'gazette_notices', q=q, **kwargs)

    def search_control_statements(self, q, **kwargs):
        return self.search('statements', 'control_statements', q=q, **kwargs)

    def fetch_statement(self, identifier, **kwargs):
        return self.fetch('statements', identifier, **kwargs)

    def fetch_placeholder(self, q, *args, **kwargs):
        placeholder = self.fetch('placeholders', q, **kwargs)
        placeholder.network = self.fetch('placeholders', q,
                                         'network', **kwargs).results
        placeholder.statements = self.fetch('placeholders', q,
                                            'statements', **kwargs).results
        return placeholder

    def fetch_jurisdictions(self, **kwargs):
        return self.fetch('jurisdictions', **kwargs)


class Version04(Version):

    api_version = '0.4'
    search_types = ['companies', 'officers', 'corporate_groupings',
                    'statements', 'control_statements',
                    'trademark_registrations', 'jurisdictions']
    fetch_types = ['companies', 'officers', 'corporate_groupings',
                   'filings', 'data', 'statements', 'placeholders',
                   'jurisdictions', 'industry_codes', 'account_status']
    match_types = ['jurisdictions']

    def __init__(self, api_token=None):
        super(Version04, self).__init__(self.api_version,
                                                self.search_types,
                                                self.fetch_types,
                                                self.match_types,
                                                api_token)

    def match_jurisdiction(self, q=None, **kwargs):
        return self.request('jurisdictions', q=q, **kwargs)

    def search_trademark_registrations(self, q, **kwargs):
        return self.search('statements', 'trademark_registrations', q=q, **kwargs)


# build versions dict by instantiating class objects
global_objs = list(globals().items())
for name, obj in global_objs:
    if obj is not Version and isinstance(obj, type) and issubclass(obj, Version):
        obj()