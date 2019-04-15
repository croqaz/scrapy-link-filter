import logging
from typing import Optional

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


def create_link_extractor(rules: str) -> Optional[LinkExtractor]:
    """
    Use the extraction rules defined per URL
    and return a new FilteringLinkExtractor.
    """
    if not rules:
        return
    # Use these fields, ignore the rest
    fields = ('allow', 'deny', 'allow_domains', 'deny_domains')
    fixed_rules = {k: rules.get(k) for k in fields if rules.get(k)}
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

    def process_spider_output(self, response, result, spider):
        extractor = None
        if isinstance(getattr(spider, 'extract_rules', False), dict):
            rules = spider.extract_rules
            logger.debug('Using extract rules: %s', rules, extra={'spider': spider})
            extractor = create_link_extractor(rules)

        def _filter(request):
            if extractor and isinstance(request, Request) and not extractor.matches(request.url):
                logger.debug('Dropping link: %s', request.url, extra={'spider': spider})
                self.crawler.stats.inc_value('link_filtering/dropped_requests')
                return False
            return True

        return (r for r in result or () if _filter(r))


SPIDER_MIDDLEWARES = {
    'link_filter.LinkFilterMiddleware': 950,
}
