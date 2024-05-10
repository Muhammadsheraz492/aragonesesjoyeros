import re

import scrapy


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["aragonesesjoyeros.com"]
    start_urls = ["https://aragonesesjoyeros.com/anillos/compromiso-58/"]
    # start_urls = ["https://aragonesesjoyeros.com/anillos/diamantes/anillo-media-alianza-de-oro-blanco-con-9-diamantes"]
    #
    def parse(self, response):
        print(response.status)

        urls = response.xpath(
            '//div[@class="thumbnail-container"]/a/@href').getall()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_detail)
    def parse_detail(self, response):
        url=response.url
        path=response.xpath("//ol/li//span/text()").getall()
        title=response.xpath("//h1/span/text()").getall()
        price=response.xpath('//*[@id="col-product-info"]/div[1]/div/div[1]/div/span/span/text()').get()
        description = response.xpath('//div[contains(@class, "rte-content") and contains(@class, "product-description")]/text()').get()
        image=response.xpath('//img/@src').get()
        product_info = {}
        data_sheet = response.css('section.product-features dl.data-sheet')
        dt_elements = data_sheet.css('dt.name')
        dd_elements = data_sheet.css('dd.value')
        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.css('::text').get().strip()
            value = dd.css('::text').get().strip()
            product_info[key] = value

        print(price)
        product_info_str = ",".join([f"{key}: {value}" for key, value in product_info.items()])

        yield {
            "image_url": image,
            "category":'/'.join(path),
            "title":"".join(title),
            "price": price.replace("\n","").replace("\xa0",""),
            "description":description,
            "product-features":product_info_str,
            "url":url
        }


        pass