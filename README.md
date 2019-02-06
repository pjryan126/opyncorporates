![](https://i.imgur.com/uxkd2sh.png)

<img src="https://travis-ci.com/pjryan126/opyncorporates.svg?token=VzzyyiUM2zPeDsfHmFKf&branch=master">

# opyncorporates
A Python package for accessing the OpenCorporates API

# Overview

`opyncorporates` is a Python wrapper around the OpenCorporates API. The wrapper
allows a user to create an instance of an opyncorporates "Engine," which allows
the user to interact with the OpenCorporates API through two simple methods: 
`search` and `fetch`.

The `search` and `fetch` methods use signatures that aim to mimic the
request arguments and variables required in the GET requests through the 
OpenCorporates API, while eliminating some of the cruft.

For example, a request to search for a company by name through the 
OpenCorporates API might look something like this:

`GET https://api.opencorporates.com/v0.4/companies/search?q=bar&per_page=100`

Submitting the same request through the search method of of an opyncorporates 
Engine object, on the other hand, would look like this:

```
from opyncorporates import create_engine

engine = create_engine(api_version='0.4')
search = engine.search('companies', q='bar', per_page=100)
```

Both the `search` and `fetch` methods return opyncorporates.Request objects,
which allow the user (1) to explore information related to a request and (2) to
obtain results more easily than it would be to craft a series of successive API 
calls. 

# Getting Started
