# Scrapy-link-filter

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Spider Middleware that allows a [Scrapy Spider](https://scrapy.readthedocs.io/en/latest/topics/spiders.html) to filter requests.
There is similar functionality in the [CrawlSpider](https://scrapy.readthedocs.io/en/latest/topics/spiders.html#crawlspider) already using Rules and in the [RobotsTxtMiddleware](https://scrapy.readthedocs.io/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.robotstxt), but there are twists.
This middleware allows defining rules dinamically per spider, or job, or request.


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


Example of a specific allow filter:

```py
extract_rules = {"allow_domains": "example.com", "allow": "/en/items/"}
```

Or a specific deny filter:

```py
extract_rules = {
    "deny_domains": ["whatever.com", "ignore.me"],
    "deny": ["/privacy-policy/?$", "/about-?(us)?$"]
}
```

The allowed fields are:
* `allow_domains` and `deny_domains` - one, or more domains to specifically limit to, or specifically reject
* `allow` and `deny` - one, or more sub-strings, or patterns to specifically allow, or reject

-----

## License

[BSD3](LICENSE) © Cristi Constantin.
