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
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )

    def parse(self, response):
        urls = response.xpath('//a[@class="overlay"]/@href').extract()
        for url in urls:
            producer.send("test", url)
            sleep(0.5)


