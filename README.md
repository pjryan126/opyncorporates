<img src="https://i.imgur.com/uxkd2sh.png" alt="opyncorporates" width="512"/>

[![Travis](https://travis-ci.com/pjryan126/opyncorporates.svg?branch=master)](https://travis-ci.com/pjryan126/opyncorporates.svg?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/pjryan126/opyncorporates.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/pjryan126/opyncorporates/alerts/) 
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/pjryan126/opyncorporates.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/pjryan126/opyncorporates/context:python)

# Overview

`opyncorporates` is a Python wrapper for the [OpenCorporates API](https://api.opencorporates.com).
It allows a user to create an `Engine` object that interacts with the API 
through two simple methods: `search` and `fetch`.

The `search` and `fetch` methods use signatures that mimic the request 
arguments and variables required in the GET requests through the  
[OpenCorporates API](https://api.opencorporates.com), 
while eliminating some of the cruft.

For example, a request to search for a company by name through the 
[OpenCorporates API](https://api.opencorporates.com) 
might look something like this:

`GET https://api.opencorporates.com/v0.4/companies/search?q=bar&per_page=100`

Submitting the same request through the search method of of an opyncorporates 
Engine object, on the other hand, would look like this:

```
>>> from opyncorporates import create_engine
>>> engine = create_engine(api_version='0.4')
>>> search = engine.search('companies', q='bar', per_page=100)
```

Both the `search` and `fetch` methods return `opyncorporates.Request` objects,
which allow the user (1) to explore information related to a request and (2) to
obtain results more easily than it would be to craft a series of successive API 
calls. 

# Getting Started

This section will show you how to get up and running with the 
`opyncorporates` package. Additional information can be found in the 
documentation [here](https://opyncorporates.readthedocs.io/en/latest/).

To get started, you can install the package using ``pip``:

```
$ pip install opyncorporates
```

Once the package is installed, you can use it to create an
`Engine` object for submitting requests and retrieving data through the 
OpenCorporates API. When creating an `Engine` object, you have the option of 
specifying an API version and an API token:
 
 ```
>>> from opyncorporates import create_engine
>>> engine = create_engine(api_version='0.4',
...                        api_token='<api-token>')
>>> engine.api_version
'0.4'
```

The API version and API token will be used when building the urls required to
submit requests to the [OpenCorporates API](https://api.opencorporates.com). 
As of now, the package's default API version is 0.4, and it is the only 
version supported. If you are planning to query the API on a regular basis, I
highly recommend purchasing an API token to increase your call limits.

Once you have created an `Engine` object, you
can start making calls to the [OpenCorporates API](https://api.opencorporates.com). 
In general, each of your API calls will perform only one of two actions. It 
will either:

1. **search** for potential matches to a specified string value, or
2. **fetch** a specific object by its unique identifier

There is a third action available when seeking information about a particular
object using an imprecise identifier. This third action allows you to **match**
to an object by providing a string value for that object's name.

Finally, if none of these actions suit your purposes, you can make a generic
**request** to the API and parse the response yourself.

The call signatures for the methods associated with each action mimic HTTPS
calls to the API. Http request args are 
submitted to the method as positional arguments, while request variables are 
submitted as keyword arguments.

Further explanation of the search, fetch, match, and request actions can be
found below.

Search
------

Your `Engine` object implements searches through the `search` method, which
returns a `SearchRequest` object:

```
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
```

You can then use the properties of this `SearchRequest` object to return as 
much or as little information from the OpenCorporates database as you need. 
For example, if you want to retrieve only the first page of search results 
from the [OpenCorporates API](https://api.opencorporates.com):

```
>>> first_page = search.get_page(1)
>>> print(type(first_page))
<class 'list'>
>>> print(len(first_page))
30
>>> print(type(first_page[0]))
<class 'dict'>
```

Fetch
-----

The `fetch` method implements the second available action. This method allows
 a user to retrieve a specific item from the OpenCorporates API by providing 
 the item's type and unique identifier. For example, a user can retrieve a 
 specific company from the [OpenCorporates API](https://api.opencorporates.com)
 by providing its item type (*i.e.*, 'company' or 'companies') and its unique
 identifier, which is the company's two-character country code plus its 
 company number unique to that jurisdiction:

```
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
```

If the fetch action is successful, the item is stored as a dict in the
`FetchRequest` object's `results` attribute.

Match
-----

The `match` method implements the third available action. It allows a user to
 match a specified string value to a single item in the [OpenCorporates](https://opencorporates.com) 
 database. As of version 0.4, the [OpenCorporates API](https://api.opencorporates.com) exposes this action to 
 match jurisdictions only:

```
>>> from opyncorporates import create_engine
>>> engine = create_engine()
>>> match = engine.match('jurisdictions', q='U.K.')
```

Request
-------

The `request` method implements a generic request action. It allows a user to
 submit a request by supplying either (1) a string for the request args 
 and/or vars or (2) the request arguments and variables as positional and 
 keyword parameters. The engine will build a clean url for your request.

 For example, the same request for a search of company records can be written
  in any of the following ways:

```
>>> from opyncorporates import create_engine
>>> engine = create_engine()
>>> r1 = engine.request('companies/gb/00102498/search?q=google')
>>> r2 = engine.request('/companies/gb/00102498/search',
...                    q='Google')
>>> r3 = engine.request('companies', 'gb', '00102498', 'search'
...                    q='google')
>>> r1.url == r2.url == r3.url # confirm all urls are the same
True
```