# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import os
from time import time
from time import sleep
import json
from scrapy.crawler import CrawlerProcess

from kafka import KafkaProducer
from itertools import chain

def create_message(title):
    msg = {
        "time": int(time() * 1000.0),
        "msg": title
    }

    return msg

    # one broker is enough
KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                             value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                             client_id="Simple Producer")



class JobsSpider(scrapy.Spider):
    name = "jobs"
    pages_V = set()
    urls_V = set()
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )

    def parse(self, response):


        url1s = response.xpath('//a[@class="overlay"]/@href').extract()
        url2s = response.xpath('//h2/a/@href').extract()

        pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()

        for url in chain(url1s, url2s):
            if "/2016/" in url:
                self.finished = True
            absolute_url = response.urljoin(url)
            if (absolute_url not in self.urls_V):
                self.urls_V.add(absolute_url)

                yield Request(absolute_url, callback=self.parse_page,
                              meta={'URL': absolute_url})
        for page in pages:
            absolute_page = response.urljoin(page)
            if (absolute_page not in self.pages_V):
                self.pages_V.add(absolute_page)
                yield Request(absolute_page , callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        message = create_message(article_title)
        producer.send("test", message)


if __name__ == "__main__":
    process = CrawlerProcess({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    })

    process.crawl(JobsSpider)
    process.start()

