# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import pymysql
import time
from ..import settings
from ..items import NewsReportItem
from ..utils.langconv import Converter
import re


class OrientaldailySpider(scrapy.Spider):
    name = 'orientaldaily'
    allowed_domains = ['orientaldaily.on.cc']
    custom_settings = {
        'ITEM_PIPELINES': {
            'news_search.pipelines.NewsSitePipeline': 200,
        }
    }


    def __init__(self, *args, **kwargs):
        conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                               passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT url FROM google WHERE site = '{}'".format(
            "orientaldaily.on.cc")
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()
        self.start_urls = [x[0] for x in data]


    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = NewsReportItem()
        try:
            title = soup.select_one('h1')
            item['title'] = Converter('zh-hans').convert(title.text)
        except Exception as e:
            print(e)
            return
        # print(title)
        item['url'] = response.url

        # 获取正文内容
        cl_names = ['#contentCTN-right']
        isCorrect = False
        content = []
        for cl in cl_names:
            content = soup.select('%s > p,h3' % cl)
            # print(len(content))
            if len(content) > 0:
                isCorrect = True
                break
        if isCorrect is False:
            print('[网页格式错误]')
            return

        item['content'] = ''
        for line in content:
            item['content'] += line.text.strip().replace(u'\u3000',
                                                         ' ').replace(u'\xa0', ' ')
        item['content'] = Converter('zh-hans').convert(item['content'])
        # print(item['content'])

        # 日期
        pat = re.compile(r"\d{8}")
        date = pat.search(response.url).group()
        # print(date)
        if date is not None:
            item['date'] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.strptime(date, r'%Y%m%d'))
        # print(item['date'])
        # return
        yield item
        return
