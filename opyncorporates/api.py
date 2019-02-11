from datetime import datetime
import json
import requests

BASE_URL = 'https://api.opencorporates.com'


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

        self.args = list(args)
        self.vars = kwargs
        self.api_token = kwargs.get('api_token', None)
        self.url = None
        self.responses = []

        # select build method
        print(self.args[0])
        is_http = str(self.args[0]).startswith('http://api.opencorporates.com')
        is_https = str(self.args[0]).startswith(
            'https://api.opencorporates.com')
        if is_http or is_https:
            url = self.args.pop(0)
            route = url.replace('https://', '').replace('http://', '')
            route = route.split('/', 1)[1]
            self.__build_from_route(route, *self.args, **self.vars)
        elif len(args) == 1 and '/' in args[0]:
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

    def __build(self, api_version, *args, **kwargs):
        """ Build the Request object using args and kwargs provided."""

        self.api_token = None
        self.api_version = str(api_version).replace('v', '')
        self.args = list(args)
        self.vars = kwargs or {}

        # get api_token if provided
        self.api_token = kwargs.get('api_token', None)
        if 'api_token' in kwargs.keys() and kwargs.get('api_token') is None:
            del kwargs['api_token']

        # clean query term for request url
        if self.vars.get('q', None):
            self.vars['q'] = self.vars['q'].lower().replace(' ', '+')

        # build request url
        self.url = "%s/v%s/" % (BASE_URL, self.api_version)
        self.url += '/'.join([str(a) for a in self.args])
        if self.vars is not None:
            self.url += '?'
            self.url += '&'.join(['%s=%s' % (k, v) for k, v in
                                  self.vars.items()])

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


class FetchRequest(Request):
    """ Get an item from the opencorporates API by unique identifier.

    In most cases, a unique identifying number is provided after the object
    type. When selecting companies, however, the company's two-character
    country code must be supplied, too.

    Notes
    -----
    See https://api.opencorporates.com/documentation/API-Reference for
    additional information on available arguments and keyword arguments.

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
        self.results = None

        api_version = str(api_version).replace('v', '')

        # construct args
        args = list(args)
        args.insert(0, "v%s" % api_version)
        args.insert(1, self.object_type)

        super(FetchRequest, self).__init__(*args, **kwargs)

        if self.response.status_code == 200:
            response_text = json.loads(self.response.text)
            if len(response_text['results']) == 0:
                self.results = []
            else:
                self.results = list(response_text['results'].values())[0]


class MatchRequest(Request):
    """ Submits a match request to the opencorporates API.

    The MatchRequest class is a subclass of the Request class. Like
    the Request class, the Search class is intended to mimic the
    opencorporates REST API syntax. Request args (i.e. arguments separated
    by '/' characters following the base url) are provided as positional
    arguments, and request vars (i.e., key-value pairs following the '?'
    character in the url and separated by '&' characters) are provided as
    keyword arguments.

    Notes
    -----
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
    object_type: str
        The type of object to search for.
    search_term: str
        The original term provided for the match request.
    q: str
        The match term transformed for use in the request url.
    results: dict
        The results of the match request.
    """

    def __init__(self, cls, api_version, object_type, *args, **kwargs):

        q = kwargs.pop('q', None)
        if q is None:
            raise ValueError('Enter a term for your match request.')

        self._cls = cls
        self.object_type = object_type
        self.match_term = q
        self.q = q.lower().replace(' ', '+')
        self.results = {}

        api_version = str(api_version).replace('v', '')

        # construct args
        args = list(args)
        args.insert(0, "v%s" % api_version)
        args.insert(1, self.object_type)
        args.append('match')

        # construct kwargs
        kwargs['q'] = self.q

        super(MatchRequest, self).__init__(*args, **kwargs)

        if self.response.status_code == 200:
            response_text = json.loads(self.response.text)
            self.results = list(response_text['results'].values())[0]
            self.results = [r for r in self.results]


class SearchRequest(Request):
    """ Submits a search request to the opencorporates API.

    The SearchRequest class is a subclass of the Request class. Like
    the Request class, the Search class is intended to mimic the
    opencorporates REST API syntax. Request args (i.e. arguments separated
    by '/' characters following the base url) are provided as positional
    arguments, and request vars (i.e., key-value pairs following the '?'
    character in the url and separated by '&' characters) are provided as
    keyword arguments.

    Search results are provided in a paginated format. Each page of the
    search results is obtained through a separate request to the
    opencorporates API with page=X supplied as a request variable.

    Notes
    -----
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

    def __init__(self, api_version, object_type, *args, **kwargs):

        q = kwargs.pop('q', None)
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
        args.insert(0, "v%s" % api_version)
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
            self.page_urls = ["%s&page=%s" % (self.url, p + 1) for p in range(self.total_pages)]

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

        url = self.url + '&page=%s' % page

        response = requests.get(url)
        if response.status_code == 200:
            res = json.loads(response.text)['results'][self.object_type]
            items = []
            for item in res:
                for k,v in item.items():
                    items.append(v)
            return items
