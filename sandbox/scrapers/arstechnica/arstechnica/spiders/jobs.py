# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import os
from time import time
from time import sleep
import json


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
    V = set()
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )

    def parse(self, response):

        def process_url(response, url):
            absolute_url = response.urljoin(url)
            producer.send("test", absolute_url)
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
            if (absolute_page not in self.V):
                self.V.add(absolute_page)
                yield Request(absolute_page , callback=self.parse)





