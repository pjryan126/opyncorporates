from datetime import datetime
import json
import requests

from bunch import Bunch

API_VERSION = '0.4'
BASE_URL = 'https://api.opencorporates.com'
SEARCH_TYPES = ['companies', 'officers', 'corporate_groupings', 'statements']


class Request(object):
    """ An object for consuming the opencorporates API.

        A user can instantiate a Request object in any one of the following
        three ways:

            -   provide the complete request url as the first and only argument
            -   provide the route url (i.e., the portion of the url following
                https://api.opencorporates.com) as the first and only argument
            -   provide the request args as positional arguments and key-value
                pairs as keyword arguments

        The last way is intended to mimic the opencorporates REST API syntax.
        Request args (i.e. arguments separated by '/' characters following the
        base url) are provided as positional arguments, and request vars (i.e.,
        key-value pairs following the '?' character in the url and
        separated by '&' characters) are provided as keyword arguments.

        Examples
        -------
        https://api.opencorporates.com/v0.4/companies/search?q=google -->
            Request('https://api.opencorporates.com/v0.4/companies/search?q=google')
            Request('/v0.4/companies/search?q=google')
            Request('v0.4', 'companies', 'search', q='Google')

        Notes
        -----
        See https://api.opencorporates.com/documentation/API-Reference for
        additional information on available arguments and keyword arguments.

        Attributes
        ----------
        _request_args:
            The list of args used in the request.
        _request_vars:
            The list of key-value variables used in the request.
        api_version: str
            The API version used for the request.
        api_token: str
            The API token used for the request.
        object_type: str
            The type of object associated with the request.
        url: str
            The url for the request.
        responses: list
            A list of all responses objects returned by the Request object.

    """

    def __init__(self, *args, **kwargs):

        self.api_version = API_VERSION
        self.api_token = None
        self.args = list(args)
        self.vars = kwargs
        self.url = None
        self.responses = []

        # select build method
        if 'api.opencorporates.com' in str(self.args[0]):
            url = self.args.pop(0)
            route = url.replace('https://', '').replace('http', '').split('/', 1)[1]
            self.__build_from_route(route, *self.args, **self.vars)
        elif len(args) == 1 and ('/') in args[0]:
            self.__build_from_route(*args, **self.vars)
        else:
            self.api_version = self.args.pop(0)
            self.__build(self.api_version, *self.args, **self.vars)

    @property
    def response(self):
        """ Returns the most current response for the request.

        Returns
        -------
        response: obj
            A requests.Models.Response object with a requested_at attribute.

        """

        if len(self.responses) == 0:
            self.get_response()

        return self.responses[-1]

    def get_response(self):
        """ Submits the request to the opencorporates API.

        When called, this method submits the request to the opencorporates API
        and appends it to the responses attribute.

        Returns
        -------
        response: obj
            A requests.Models.Response object with a requested_at attribute.

        """
        response = requests.get(self.url)
        response.requested_at = datetime.utcnow()
        self.responses.append(response)
        return response

    def __build(self, *args, **kwargs):
        """ Build the Request object using args and kwargs provided."""

        self.api_token = None
        self.api_version = API_VERSION
        self.args = list(args)
        self.vars = kwargs or None

        # get api_version if listed in args
        if '.' in str(self.args[0]):
            self.api_version = str(self.args.pop(0)).replace('v', '')

        # get api_token if provided
        self.api_token = kwargs.get('api_token', None)

        # clean query term for request url
        if 'q' in self.vars.keys():
            self.vars['q'] = self.vars['q'].lower().replace(' ', '+')

        # build request url
        self.url = f"{BASE_URL}/v{self.api_version}/"
        self.url += '/'.join([str(a) for a in self.args])
        if self.vars is not None:
            self.url += '?'
            self.url += '&'.join([f'{k}={v}' for k, v in self.vars.items()])

    def __build_from_route(self, route, *args, **kwargs):

        """ Parse route into args and kwargs.

        This method parses a provided route string into args and kwargs and
        then submits it to the __build method to complete instantiation of the
        Request object.

        """

        if route[0] == '/':
            route = route[1:]
        request_args = route.split('/')

        request_vars = {}

        if '?' in request_args[-1]:
            request_args[-1], request_vars = request_args[-1].split('?')
            request_vars = {x[0]: x[1] for x in [x.split("=") for x in
                                                 request_vars.split("&")]}

        request_args.extend(list(args))

        for k, v in kwargs.items():
            request_vars[k] = v

        self.__build(*request_args, **request_vars)

    def __str__(self):
        """ Pretty print the Request object."""

        obj = dict()

        # remove hidden key-value pairs
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                obj[k] = v

        return json.dumps(obj, indent=4, sort_keys=True)


class SearchRequest(Request):
    """ Submits a search request to the opencorporates API.

    The Search class is a subclass of the Request class. Like instantation
    the Request class, the Search class is intended to mimic the
    opencorporates REST API syntax. Request args (i.e. arguments separated
    by '/' characters following the base url) are provided as positional
    arguments, and request vars (i.e., key-value pairs following the '?'
    character in the url and separated by '&' characters) are provided as
    keyword arguments.

    Search results are provided in a paginated format. Each page of the
    search results is obtained through a separate request to the
    opencorporates API with page=X supplied as a request variable.

    Note
    ----
    See https://api.opencorporates.com/documentation/API-Reference for
    additional information on available arguments and keyword arguments.

    Parameters
    ----------
    api_version: str
        The API version used for the request
    object_type: str
        The type of object to search for.
    q: str (optional)
        The term that you are searching for

    Attributes
    ----------
    In addition to the attributes exposed by the Request class:

    api_version: str
        The API version used for the request
    object_type: str
        The type of object to search for.
    search_term: str
        The original term provided for the search
    q: str
        The search term transformed for use in the request url
    per_page: int
        The number of search results per page
    total_pages: int
        The total number of pages of search results
    total_count: int
        The total number of search results
    page_urls: list
        A list of all request urls for obtaining the search results

    """

    def __init__(self, api_version, object_type, *args, q=None, **kwargs):

        if q is None:
            raise ValueError('Enter a term for your search')

        self.object_type = object_type
        self.search_term = q
        self.q = q.lower().replace(' ', '+')
        self.per_page = None
        self.total_pages = None
        self.total_count = None
        self.page_urls = []

        api_version = str(api_version).replace('v', '')

        # construct args
        args = list(args)
        args.insert(0, f"v{api_version}")
        args.insert(1, self.object_type)
        args.append('search')

        # construct kwargs
        kwargs['q'] = self.q

        super(SearchRequest, self).__init__(*args, **kwargs)

        if self.response.status_code == 200:
            results = json.loads(self.response.text)['results']
            self.per_page = int(results['per_page'])
            self.total_pages = int(results['total_pages'])
            self.total_count = int(results['total_count'])
            self.page_urls = [f"{self.url}&page={p+1}" for p in range(self.total_pages)]

    @property
    def results(self):
        """ Yields all search results.

        Yields
        ------
        item: dict
            A dictionary representing a search result item.

        """
        for p in self.page_urls:
            page = self.get_page(p)
            for item in page:
                yield item
        return

    def get_page(self, page):
        """ Calls the opencorporates API and returns a page of results.

        Parameters
        ----------
        page : int
            the page of search results to return.

        Returns
        -------
        list
            A list of dict objects

        """

        url = self.url + f'&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            res = json.loads(response.text)['results'][self.object_type]
            items = []
            for item in res:
                for k,v in item.items():
                    items.append(v)
            return items


class FetchRequest(Request):
    """ Get an item from the opencorporates API by unique identifier.

    In most cases, a unique identifying number is provided after the object
    type. When selecting companies, however, the company's two-character
    country code must be supplied, too.

    Examples
    --------
    officer = FetchRequest('v0.4', 'officers', '123456')
    company = FetchRequest('v0.4', 'companies', 'gb', '00102498')

    Parameters
    ----------
    api_version: str
        The API version used for the request
    object_type: str
        The type of object to search for.

    Attributes
    ----------
    object_type: str
        The requested object's type.
    results: dict
        The requested item.

    """

    def __init__(self, api_version, object_type, *args, **kwargs):

        self.object_type = object_type
        self.results = {}

        api_version = str(api_version).replace('v', '')

        # construct args
        args = list(args)
        args.insert(0, f"v{api_version}")
        args.insert(1, self.object_type)

        super(FetchRequest, self).__init__(*args, **kwargs)

        if self.response.status_code == 200:
            response_text = json.loads(self.response.text)
            self.results = list(response_text['results'].values())[0]


class Engine(object):
    """ Director for requesting and consuming opencorporates API data.

    Allows user to declare api_version and api_token values once for all
    requests, to search for specific object types, and to request specific
    items by supplying an item id.

    Note
    ----
    See https://api.opencorporates.com/documentation/API-Reference for
    additional information on available arguments and keyword arguments.

    Parameters
    ----------
    api_token: str (optional)
        The API token used for the request.
    api_version: str (optional)
        The API version used for the request.

    Attributes
    ----------
    api_version: str
        The API version used for the request.
    api_token: str
        The API token used for the request.

    """

    _SEARCH_TYPES = SEARCH_TYPES

    def __init__(self, api_token=None, api_version=API_VERSION):

        self.api_token = api_token
        self.api_version = api_version

    def get(self, *args, **kwargs):
        """ A wrapper for the Request object.

        Returns
        -------
        Request
            An object for consuming the opencorporates API.

        """
        return Request(*args, **kwargs)

    def search(self, object_type, *args, q=None, **kwargs):

        if object_type not in self._SEARCH_TYPES:
            raise ValueError(f"Please provide a valid object type as your first argument: "
                             f"({self._SEARCH_TYPES}")
        if q is None:
            raise ValueError("Please supply a search term as kwarg['q']")

        # construct args
        args = list(args)
        args.insert(0, f'v{self.api_version}')
        args.insert(1, object_type)

        # construct kwargs
        if self.api_token is not None:
            kwargs['api_token'] = self.api_token

        return SearchRequest(*args, q=q, **kwargs)

    def search_company(self, q, **kwargs):
        return self.search('companies', q=q, **kwargs)

    def search_officer(self, q, **kwargs):
        return self.search('officers', q=q, **kwargs)

    def fetch(self, object_type, *args, **kwargs):
        return FetchRequest(object_type, *args, **kwargs)


def create_engine(api_token=None, api_version=API_VERSION):
    """ Factory function to create an Engine object.

    The factory function is perfunctory and exists to handle possible changes
    to the opencorporates API in ubsequent API versions.

    Parameters
    ----------
    api_token: str (optional)
        The API token used for the request.
    api_version: str (optional)
        The API version used for the request.

    """

    engine = Engine(api_token, api_version)

    return engine
