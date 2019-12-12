# Scrapy-link-filter

  [![Python ver][python-image]][python-url]
  [![Build Status][build-image]][build-url]
  [![Code coverage][cover-image]][cover-url]
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Spider Middleware that allows a [Scrapy Spider](https://scrapy.readthedocs.io/en/latest/topics/spiders.html) to filter requests.
There is similar functionality in the [CrawlSpider](https://scrapy.readthedocs.io/en/latest/topics/spiders.html#crawlspider) already using Rules and in the [RobotsTxtMiddleware](https://scrapy.readthedocs.io/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.robotstxt), but there are twists.
This middleware allows defining rules dinamically per request, or as spider arguments instead of project settings.


## Install

This project requires [Python 3.6+](https://www.python.org/) and [pip](https://pip.pypa.io/). Using a [virtual environment](https://virtualenv.pypa.io/) is strongly encouraged.

```sh
$ pip install git+https://github.com/croqaz/scrapy-link-filter
```


## Usage

For the middleware to be enabled as a Spider Middleware, it must be added in the project `settings.py`:

```
SPIDER_MIDDLEWARES = {
    # maybe other Spider Middlewares ...
    # can go after DepthMiddleware: 900
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 950,
}
```

Or, it can be enabled as a Downloader Middleware, in the project `settings.py`:

```
DOWNLOADER_MIDDLEWARES = {
    # maybe other Downloader Middlewares ...
    # can go before RobotsTxtMiddleware: 100
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 50,
}
```

The rules must be defined either in the spider instance, in a `spider.extract_rules` dict, or per request, in `request.meta['extract_rules']`.
Internally, the extract_rules dict is converted into a [LinkExtractor](https://docs.scrapy.org/en/latest/topics/link-extractors.html), which is used to match the requests.

**Note** that the URL matching is case-sensitive by default, which works in most cases. To enable case-insensitive matching, you can specify a "(?i)" inline flag in the beggining of each "allow", or "deny" rule that needs to be case-insensitive.


Example of a specific allow filter, on a spider instance:

```py
from scrapy.spiders import Spider

class MySpider(Spider):
    extract_rules = {"allow_domains": "example.com", "allow": "/en/items/"}
```

Or a specific deny filter, inside a request meta:

```py
request.meta['extract_rules'] = {
    "deny_domains": ["whatever.com", "ignore.me"],
    "deny": ["/privacy-policy/?$", "/about-?(us)?$"]
}
```

The possible fields are:
* `allow_domains` and `deny_domains` - one, or more domains to specifically limit to, or specifically reject
* `allow` and `deny` - one, or more sub-strings, or patterns to specifically allow, or reject

All fields can be defined as string, list, set, or tuple.

-----

## License

[BSD3](LICENSE) © Cristi Constantin.


[build-image]: https://github.com/croqaz/scrapy-link-filter/workflows/Python/badge.svg
[build-url]: https://github.com/croqaz/scrapy-link-filter/actions
[cover-image]: https://codecov.io/gh/croqaz/scrapy-link-filter/branch/master/graph/badge.svg
[cover-url]: https://codecov.io/gh/croqaz/scrapy-link-filter
[python-image]: https://img.shields.io/badge/Python-3.6-blue.svg
[python-url]: https://python.org
