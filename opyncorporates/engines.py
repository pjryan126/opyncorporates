import abc
import json

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

engines = {}


class EngineAbstract(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request(self):
        """Required Method"""

    @abc.abstractmethod
    def match(self, object_type, q=None, *args, **kwargs):
        """Required Method"""

    @abc.abstractmethod
    def search(self, object_type, q=None, *args, **kwargs):
        """Required Method"""

    @abc.abstractmethod
    def fetch(self, object_type, *args, **kwargs):
        """Required Method"""


class BaseEngine(EngineAbstract):

    def __init__(self, api_version, search_types, fetch_types,
                 match_types, api_token):

        self.api_version = api_version
        self.api_token = api_token
        self.search_types = search_types
        self.fetch_types = fetch_types
        self.match_types = match_types

        engines[self.api_version] = self.__class__

    def request(self, *args, **kwargs):
        return Request(*args, **kwargs)

    def match(self, *args, **kwargs):
        return

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


class EngineV04(BaseEngine):
    """ Engine for Version 0.4 API requests.


    """
    def __init__(self, api_token=None):

        api_version = '0.4'

        search_types = [
            'companies',
            'officers',
            'corporate_groupings',
            'statements',
            'control_statements',
            'trademark_registrations',
            'jurisdictions'
        ]

        fetch_types = [
            'companies',
            'officers',
            'corporate_groupings',
            'filings',
            'statements',
            'placeholders',
            'jurisdictions',
            'industry_codes',
            'account_status'
        ]

        match_types = ['jurisdictions']

        super(EngineV04, self).__init__(api_version, search_types, fetch_types,
                                     match_types, api_token)


# build versions dict by instantiating class objects
global_objs = list(globals().items())
for name, obj in global_objs:
    if obj is not BaseEngine and isinstance(obj, type) and issubclass(obj, BaseEngine):
        obj()