.. opyncorporates documentation master file, created by
   sphinx-quickstart on Fri Sep 14 14:59:14 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://i.imgur.com/uxkd2sh.png =512x
   :width: 512px

-------------------------------------

OpynCorporates
==============


The ``opyncorporates`` package is a toolkit for working with the
`OpenCorporates <https://opencorporates.com>`_ API. which provides access to
the largest open database of companies and company data in the world, with in
excess of 100 million companies in a similarly large number of jurisdictions.
The organization's primary goal is to make information on companies more usable
and more widely available for the public benefit, particularly to tackle the
use of companies for criminal or anti-social purposes, for example corruption,
money laundering and organised crime.

Getting Started
---------------

This section will show you how to get up and running with the
``opyncorporates`` package.

To get started, you can install the package using ``pip``::

   pip install opyncorporates

Once the package is installed, you can use it to create an
:class:`~opyncorporates.engines.Engine` object for submitting requests and
retrieving data through the OpenCorporates API. When creating an
:class:`~opyncorporates.engines.Engine` object, you have the option of
specifying an API version and an API token:

.. doctest::

   >>> from opyncorporates import create_engine
   >>> engine = create_engine(api_version='0.4',
   ...                        api_token='<api-token>')
   >>> engine.api_version
   '0.4'

The API version and API token will be used when building the urls required to
submit requests to the OpenCorporates API. As of now, the package's default API
version is 0.4, and it is the only version supported. If you are planning to
query the API on a regular basis, I highly recommend purchasing an API token to
increase your call limits.

Once you have created an :class:`~opyncorporates.engines.Engine` object, you
can start making calls to the OpenCorporates API. In general, each of your API
calls will perform only one of two actions. It will either:

1. **search** for potential matches to a specified string value, or
2. **fetch** a specific object by its unique identifier

There is a third action available when seeking information about a particular
object using an imprecise identifier. This third action allows you to **match**
to an object by providing a string value for that object's name.

Finally, if none of these actions suit your purposes, you can make a generic
**request** to the API and parse the response yourself.

The call signatures for the methods associated with each action mimic HTTPS
calls to the API. Http request args are submitted to the method as positional
arguments, while request variables are submitted as keyword arguments.

Further explanation of the search, fetch, match, and request actions can be
found below.

Search
------

Your :class:`~opyncorporates.engines.Engine` object implements searches
through the :meth:`~opyncorporates.engines.Engine.search` method, which
returns a :class:`~opyncorporates.api.SearchRequest` object:

.. doctest::

   >>> from opyncorporates import create_engine
   >>> engine = create_engine(api_version='0.4')
   >>> search = engine.search('companies', 'search', q='Google')
   >>> search.url
   'https://api.opencorporates.com/v0.4/companies/search?q=google'
   >>> search.responses # a history of responses for the object
   [<Response [200]>]
   >>> search.response # the most recent response for this request
   <Response [200]>
   >>> search.total_pages
   26
   >>> search.per_page
   30
   >>> search.total_count
   764

You can then use the properties of this :class:`~opyncorporates.api
.SearchRequest` object to return as much or as little information from the
OpenCorporates database as you need. For example, if you want to retrieve
only the first page of search results from the OpenCorporates API:

.. doctest::

   >>> first_page = search.get_page(1)
   >>> print(type(first_page))
   <class 'list'>
   >>> print(len(first_page))
   30
   >>> print(type(first_page[0]))
   <class 'dict'>

Fetch
-----

The :meth:`~opyncorporates.engines.Engine.fetch` method implements the second
available action. This method allows a user to retrieve a specific item from the
OpenCorporates API by providing the item's type and unique identifier. For
example, a user can retrieve a specific company from the API by providing its
item type (*i.e.*, 'company' or 'companies') and its unique identifier, which
according to the OpenCorporates API is the company's two-character country code
plus its company number unique to that jurisdiction:

.. doctest::

   >>> from opyncorporates import create_engine
   >>> engine = create_engine(api_version='0.4')
   >>> fetch = engine.fetch('companies', 'gb', '00102498')
   >>> fetch.responses # a history of responses for the object
   [<Response [200]>]
   >>> fetch.response # the most recent response for this request
   <Response [200]>
   >>> fetch.results['name']
   'BP P.L.C.'
   >>> fetch.results['incorporation_date']
   '1909-04-14'

If the fetch action is successful, the item is stored as a dict in the
:class:`~opyncorporates.api.FetchRequest` object's :attr:`~opyncorporates
.api.FetchRequest.results` attribute.

Match
-----

The :meth:`~opyncorporates.engines.Engine.match` method implements the third
available action. It allows a user to match a specified string value to a
single item in the OpenCorporates database. As of version 0.4, the
OpenCorporates API exposes this action to match jurisdictions only:

.. doctest::

    >>> from opyncorporates import create_engine
    >>> engine = create_engine()
    >>> match = engine.match('jurisdictions', q='U.K.')

Request
-------

The :meth:`opyncorporates.engines.Engine.request` method implements a generic
 request action. It allows a user to submit a request by supplying either (1) a
 string for the request args and/or vars or (2) the request arguments and
 variables as positional and keyword parameters. The engine will build a
 clean url for your request.

 For example, the same request for a search of company records can be written
  in any of the following ways:

.. doctest::

   >>> from opyncorporates import create_engine
   >>> engine = create_engine()
   >>> r1 = engine.request('companies/gb/00102498/search?q=google')
   >>> r2 = engine.request('/companies/gb/00102498/search',
   ...                    q='Google')
   >>> r3 = engine.request('companies', 'gb', '00102498', 'search'
   ...                    q='google')
   >>> r1.url == r2.url == r3.url # confirm all urls are the same
   True


Package-level Functions
-----------------------
.. automodule:: opyncorporates
   :members:

Sub-Modules
-----------
.. toctree::
   :maxdepth: 2

   api
   engines



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
