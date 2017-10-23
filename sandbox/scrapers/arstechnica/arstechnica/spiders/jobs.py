# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )

    def parse(self, response):
        urls = response.xpath('//a[@class="overlay"]/@href').extract()
        print(urls)

