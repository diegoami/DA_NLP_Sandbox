# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

"""
class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )

    def parse(self, response):
        urls = response.xpath('//a[@class="overlay"]/@href').extract()
        pages = response.xpath('//a[@class="overlay"]/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url )

        yield Request(absolute_url , callback=self.parse_page,
                      meta={'URL': absolute_url)


    def parse_page(self, response):
        url = response.meta.get('URL')

        yield {'URL': url}


"""