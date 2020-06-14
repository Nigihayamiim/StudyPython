# -*- coding: utf-8 -*-
import scrapy


class ToobigdataSpider(scrapy.Spider):
    name = 'toobigdata'
    allowed_domains = ['toobigdata.com']
    start_urls = ['http://toobigdata.com/']

    def parse(self, response):
        pass
