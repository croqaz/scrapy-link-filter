import logging

from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


class LinkFilterMiddleware:
    """
    Downloader Middleware, or Spider Middleware,
    that allows a Scrapy Spider to filter requests.
    """

    def __init__(self, crawler):
        self.crawler = crawler
        self.debug = self.crawler.settings.getbool('LINK_FILTER_MIDDLEWARE_DEBUG', False)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        """ Called as a Downloader Middleware """
        extractor = self._create_extractor(spider, request)
        if not extractor:
            return

        if not extractor.matches(request.url):
            if self.debug:
                logger.debug('Dropping request: %s', request, extra={'spider': spider})
            self.crawler.stats.inc_value('link_filtering/downloader/dropped_requests')
            raise IgnoreRequest("Link doesn't match extract rules")

    def process_spider_output(self, response, result, spider):
        """ Called as a Spider Middleware """
        extractor = self._create_extractor(spider, response)

        def _filter(request):
            if extractor and isinstance(request, Request) and not extractor.matches(request.url):
                if self.debug:
                    logger.debug('Dropping request: %s', request, extra={'spider': spider})
                self.crawler.stats.inc_value('link_filtering/spider/dropped_requests')
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
        return LinkExtractor(**rules)


DOWNLOADER_MIDDLEWARES = {
    # It goes before RobotsTxtMiddleware: 100
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 50
}

SPIDER_MIDDLEWARES = {
    # It goes after DepthMiddleware: 900
    'scrapy_link_filter.middleware.LinkFilterMiddleware': 950
}
