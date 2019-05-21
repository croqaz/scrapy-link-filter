import re
import logging
from collections.abc import Iterable

from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.url import url_is_from_any_domain

logger = logging.getLogger(__name__)

SRE_Pattern = type(re.compile(''))


class LinkExtractor:

    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=()):

        self.allow_res = [x if isinstance(x, SRE_Pattern) else re.compile(x, re.I) \
            for x in arg_to_iter(allow)]
        self.deny_res = [x if isinstance(x, SRE_Pattern) else re.compile(x, re.I) \
            for x in arg_to_iter(deny)]

        self.allow_domains = set(arg_to_iter(allow_domains))
        self.deny_domains = set(arg_to_iter(deny_domains))

    def matches(self, url):
        if self.allow_domains and not url_is_from_any_domain(url, self.allow_domains):
            return False
        if self.deny_domains and url_is_from_any_domain(url, self.deny_domains):
            return False

        allowed = (regex.search(url) for regex in self.allow_res) if self.allow_res else [True]
        denied = (regex.search(url) for regex in self.deny_res) if self.deny_res else []

        return any(allowed) and not any(denied)


class LinkFilterMiddleware:
    """
    Spider Middleware that allows a Scrapy Spider to filter requests.
    """

    def __init__(self, crawler):
        self.crawler = crawler
        self.debug = self.crawler.settings.getbool('LINK_FILTER_MIDDLEWARE_DEBUG', False)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        """ Called as a Downloader Middleware """
        if not isinstance(getattr(spider, 'extract_rules', False), dict):
            return

        extractor = self._create_extractor(spider, request)
        if extractor and not extractor.matches(request.url.lower()):
            if self.debug:
                logger.debug('Dropping link: %s', request.url, extra={'spider': spider})
            self.crawler.stats.inc_value('link_filtering/dropped_requests')
            raise IgnoreRequest("Link doesn't match extract rules")

    def process_spider_output(self, response, result, spider):
        """ Called as a Spider Middleware """
        extractor = self._create_extractor(spider, response)

        def _filter(request):
            if extractor and isinstance(request, Request) and \
                    not extractor.matches(request.url.lower()):
                if self.debug:
                    logger.debug('Dropping link: %s', request.url, extra={'spider': spider})
                self.crawler.stats.inc_value('link_filtering/dropped_requests')
                return False
            return True

        return (r for r in result or () if _filter(r))

    def _create_extractor(self, spider, request):
        """
        Use the extraction rules defined per URL and return a new LinkExtractor.
        """
        rules = {}
        # Use the spider rules first
        if isinstance(getattr(spider, 'extract_rules', False), dict):
            rules = spider.extract_rules
        # Update the spider rules with rules from the request
        if isinstance(request.meta.get('extract_rules'), dict):
            rules.update(request.meta['extract_rules'])
        if not rules:
            return
        # Use these fields, ignore the rest
        fields = ('allow', 'deny', 'allow_domains', 'deny_domains')
        fixed_rules = {k: rules.get(k) for k in fields if isinstance(rules.get(k), Iterable)}
        if fixed_rules:
            return LinkExtractor(**fixed_rules)


DOWNLOADER_MIDDLEWARES = {
    # It goes before RobotsTxtMiddleware: 100
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 50,
}

SPIDER_MIDDLEWARES = {
    # It goes after DepthMiddleware: 900
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 950,
}
