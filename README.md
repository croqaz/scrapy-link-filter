# Scrapy-link-filter

Spider Middleware that allows a Scrapy Spider to filter requests.
There is a similar functionality in the [CrawlSpider](https://scrapy.readthedocs.io/en/latest/topics/spiders.html#crawlspider) already using Rules, but this middleware allows defining rules per job (and per domain WIP?)


## Install

This project requires [Python 3.6+](https://www.python.org/) and [pip](https://pip.pypa.io/). Using a [virtual environment](https://virtualenv.pypa.io/) is strongly encouraged.

```sh
$ pip install git+https://github.com/croqaz/scrapy-link-filter
```


## Usage

For the middleware to be enabled, it must be added in the project `settings.py`:

```
SPIDER_MIDDLEWARES = {
    # maybe other Spider Middlewares ...
    # can go after DepthMiddleware: 900
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 950,
}
```

Also, the rules must be present in the spider instance, in a `spider.extract_rules` dict, for the middleware to use them.
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
