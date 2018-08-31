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
    def search(self, object_type, *args, q=None, **kwargs):
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
                 match_types, keywords, api_token):

        self.api_version = api_version
        self.api_token = api_token
        self.search_types = search_types
        self.fetch_types = fetch_types
        self.match_types = match_types
        self.keywords = keywords

        versions[self.api_version] = self.__class__

    def request(self, *args, **kwargs):
        return Request(*args, **kwargs)

    def search(self, search_type, *args, q=None, **kwargs):

        if search_type not in self.search_types:
            msg = "`%s` not available in v%s" % (search_type, self.api_version)
            raise NotImplementedError(msg)

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
            if k in self.keywords:
                request_vars[k] = v

        return SearchRequest(*args, q=q, **request_vars)

    def search_company(self, q, **kwargs):
        return self.search('companies', q=q, **kwargs)

    def search_officer(self, q, **kwargs):
        return self.search('officers', q=q, **kwargs)

    def fetch(self, fetch_type, *args, **kwargs):
        return FetchRequest(fetch_type, *args, **kwargs)

    def fetch_company(self, jurisdiction_code, identifier, **kwargs):
        return FetchRequest('companies', jurisdiction_code, identifier, **kwargs)


class Version04(Version):

    api_version = '0.4'
    search_types = ['companies', 'officers', 'corporate_groupings',
                    'gazette_notices', 'control_statements',
                    'trademark_registrations', 'jurisdictions']
    fetch_types = ['companies', 'officers', 'corporate_groupings',
                   'filings', 'data', 'statements', 'placeholders',
                   'industry_codes', 'account_status']
    match_types = ['jurisdictions']
    keywords = []

    def __init__(self, api_token=None):
        super(Version04, self).__init__(self.api_version,
                                                self.search_types,
                                                self.fetch_types,
                                                self.match_types,
                                                self.keywords,
                                                api_token)

    def match_jurisdiction(self, q=None, **kwargs):
        return self.request('jurisdictions', q=q, **kwargs)


# build versions dict by instantiating class objects
global_objs = list(globals().items())
for name, obj in global_objs:
    if obj is not Version and isinstance(obj, type) and issubclass(obj, Version):
        obj()