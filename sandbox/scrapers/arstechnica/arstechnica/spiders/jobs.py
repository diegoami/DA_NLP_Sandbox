# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import os
from time import time
from time import sleep
import json
from scrapy.crawler import CrawlerProcess

from kafka import KafkaProducer


def create_message():
    msg = {
        "time": int(time() * 1000.0),
        "msg": "Hello, World!"
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

        def process_url(response, url):
            absolute_url = response.urljoin(url)
            if (absolute_url not in self.urls_V):
                self.urls_V.add(absolute_url)
            producer.send("arstechnica", absolute_url)
            sleep(0.5)

        url1s = response.xpath('//a[@class="overlay"]/@href').extract()
        url2s = response.xpath('//h2/a/@href').extract()

        pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()

        for url in url1s:
            process_url(response, url)

        for url in url2s:
            process_url(response, url)

        for page in pages:
            absolute_page = response.urljoin(page)
            if (absolute_page not in self.pages_V):
                self.pages_V.add(absolute_page)
                yield Request(absolute_page , callback=self.parse)





if __name__ == "__main__":
    process = CrawlerProcess({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    })

    process.crawl(JobsSpider)
    process.start()

