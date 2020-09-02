# -*- coding: utf-8 -*-
import scrapy


class OrientaldailySpider(scrapy.Spider):
    name = 'orientaldaily'
    allowed_domains = ['orientaldaily.on.cc']
    start_urls = ['http://orientaldaily.on.cc/']

    def parse(self, response):
        pass
