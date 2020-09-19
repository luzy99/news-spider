# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import pymysql
import time
from ..import settings
from ..items import NewsReportItem
from ..utils.langconv import Converter


class NytimesSpider(scrapy.Spider):
    name = 'nytimes'
    allowed_domains = ['cn.nytimes.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'news_search.pipelines.NewsSitePipeline': 200,
        }
    }

    def __init__(self, *args, **kwargs):
        conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                               passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT url FROM google WHERE site = '{}' and keyword != '逃犯条例'".format(
            "cn.nytimes.com")
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()
        self.start_urls = [x[0] for x in data]


    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = NewsReportItem()
        try:
            title = soup.select('header > h1')[-1]
            item['title'] = title.text
        except Exception as e:
            print(e)
            return
        # print(title)
        item['url'] = response.url

        # 获取正文内容
        cl_names = ['.article-body-item']
        isCorrect = False
        content = []
        for cl in cl_names:
            content = soup.select('%s > div' % cl)
            # print(len(content))
            if len(content) > 0:
                isCorrect = True
                break
        if isCorrect is False:
            print('[网页格式错误]')
            return
        # print(content)
        item['content'] = ''
        for line in content:
            item['content'] += line.text.strip().replace(u'\u3000',
                                                         ' ').replace(u'\xa0', ' ')
        # item['content'] = Converter('zh-hans').convert(item['content'])
        # print(item['content'])

        # 日期
        date = soup.select_one('time')
        if date is not None:
            item['date'] = date['datetime']
        # print(item['date'])
        yield item
        return

