# -*- coding: utf-8 -*-
import scrapy


class SingtaousaSpider(scrapy.Spider):
    name = 'singtaousa'
    allowed_domains = ['singtaousa.com']
    start_urls = ['http://singtaousa.com/']

    def parse(self, response):
        pass
