import scrapy


class XSpider(scrapy.Spider):
    name = "x"
    allowed_domains = ["myspider"]
    start_urls = ["https://myspider"]

    def parse(self, response):
        pass
