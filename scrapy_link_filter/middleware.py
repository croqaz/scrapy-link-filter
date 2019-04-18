import logging
from typing import Optional
from collections.abc import Iterable

from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


def create_link_extractor(rules: str) -> Optional[LinkExtractor]:
    """
    Use the extraction rules defined per URL
    and return a new FilteringLinkExtractor.
    Make sure the matching expressions are lower-case.
    """
    if not rules:
        return
    # Use these fields, ignore the rest
    fields = ('allow', 'deny', 'allow_domains', 'deny_domains', 'restrict_text')
    fixed_rules = {k: rules.get(k) for k in fields if isinstance(rules.get(k), Iterable)}
    if fixed_rules:
        return LinkExtractor(**fixed_rules)


class LinkFilterMiddleware:
    """
    Spider Middleware that allows a Scrapy Spider to filter requests.
    """

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        """ Called as a Downloader Middleware """
        if not isinstance(getattr(spider, 'extract_rules', False), dict):
            return

        extractor = self._create_extractor(spider, request)
        if extractor and not extractor.matches(request.url.lower()):
            logger.debug('Dropping link: %s', request.url, extra={'spider': spider})
            self.crawler.stats.inc_value('link_filtering/dropped_requests')
            raise IgnoreRequest("Link doesn't match extract rules")

    def process_spider_output(self, response, result, spider):
        """ Called as a Spider Middleware """
        extractor = self._create_extractor(spider, response)

        def _filter(request):
            if extractor and isinstance(request, Request) and \
                    not extractor.matches(request.url.lower()):
                logger.debug('Dropping link: %s', request.url, extra={'spider': spider})
                self.crawler.stats.inc_value('link_filtering/dropped_requests')
                return False
            return True

        return (r for r in result or () if _filter(r))

    def _create_extractor(self, spider, request):
        rules = {}
        if isinstance(getattr(spider, 'extract_rules', False), dict):
            rules = spider.extract_rules
        if isinstance(request.meta.get('extract_rules'), dict):
            rules.update(request.meta['extract_rules'])
        return create_link_extractor(rules)


DOWNLOADER_MIDDLEWARES = {
    # It goes before RobotsTxtMiddleware: 100
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 50,
}

SPIDER_MIDDLEWARES = {
    # It goes after DepthMiddleware: 900
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 950,
}
