import logging

from scrapy.http import Request
from scrapy.exceptions import NotConfigured
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


class LinkFilterMiddleware:
    """
    Middleware that allows a Scrapy Spider to filter requests.
    """

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('LINK_FILTER_ENABLED'):
            raise NotConfigured
        return cls(crawler)

    def process_spider_output(self, response, result, spider):
        # Inspired from DepthMiddleware
        def _filter(request):
            if isinstance(request, Request) and response.meta.get('link_filtering'):
                extractor = response.meta['link_filtering']
                if isinstance(extractor, LinkExtractor):
                    if not extractor.matches(request.url):
                        logger.debug('Dropping link: %s', request.url, extra={'spider': spider})
                        self.crawler.stats.inc_value('link_filtering/dropped_requests')
                        return False
            return True

        return (r for r in result or () if _filter(r))
