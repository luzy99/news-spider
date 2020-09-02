# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsReportItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()    # 链接
    title = scrapy.Field()  # 标题
    sourceTitle = scrapy.Field()  # 原标题
    content = scrapy.Field()  # 内容
    source = scrapy.Field()  # 来源
    date = scrapy.Field()   # 日期
    pass

class SearchResultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()    # 链接
    site = scrapy.Field()  # 站点
    keyword = scrapy.Field()  # 关键词
    pass