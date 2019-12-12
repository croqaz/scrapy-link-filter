import pytest
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler
from scrapy.exceptions import IgnoreRequest

from scrapy_link_filter.middleware import LinkFilterMiddleware


def _mock_mw(spider):
    class MockedDownloader:
        slots = {}

        def _get_slot_key(self, a, b):
            return str(a) + str(b)

    class MockedEngine:
        downloader = MockedDownloader()
        fake_spider_closed_result = None

        def close_spider(self, spider, reason):
            self.fake_spider_closed_result = (spider, reason)

    # with `spider` instead of `type(spider)` raises an exception
    crawler = get_crawler(type(spider))
    crawler.engine = MockedEngine()
    return LinkFilterMiddleware.from_crawler(crawler)


def test_disabled():
    spider = Spider('spidr')
    mw = _mock_mw(spider)

    req = Request('http://quotes.toscrape.com')
    out = mw.process_request(req, spider)
    assert out is None


def test_allow():
    spider = Spider('spidr')
    spider.extract_rules = {'allow': 'x'}
    mw = _mock_mw(spider)

    req = Request('http://quotes.toscrape.com')

    with pytest.raises(IgnoreRequest):
        mw.process_request(req, spider)

    spider.extract_rules = {'allow': 'quotes'}
    mw.process_request(req, spider)


def test_deny():
    spider = Spider('spidr')
    spider.extract_rules = {'deny': 'quotes'}
    mw = _mock_mw(spider)

    req = Request('http://quotes.toscrape.com')

    with pytest.raises(IgnoreRequest):
        mw.process_request(req, spider)

    spider.extract_rules = {'deny': 'x'}
    mw.process_request(req, spider)


def test_spider_mw():
    spider = Spider('spidr')
    spider.extract_rules = {'allow': 'quotes'}
    mw = _mock_mw(spider)

    req = Request('http://quotes.toscrape.com')

    # Requests are allowed to pass
    gen = mw.process_spider_output(req, [req], spider)
    assert list(gen) == [req]

    spider.extract_rules = {'deny': 'quotes'}

    # Requests are denied
    gen = mw.process_spider_output(req, [req], spider)
    assert list(gen) == []


def test_request_meta():
    spider = Spider('spidr')
    mw = _mock_mw(spider)

    meta = {'extract_rules': {'deny': '(?i)quotes'}}
    req = Request('http://quotes.toscrape.com', meta=meta)

    with pytest.raises(IgnoreRequest):
        mw.process_request(req, spider)
