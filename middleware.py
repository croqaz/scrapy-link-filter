import logging

from scrapy.http import Request
from scrapy.exceptions import NotConfigured

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
