# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from . import settings

class GooglePipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        self.cur = self.conn.cursor()

        sql = '''CREATE TABLE IF NOT EXISTS `job_news`.`{}`  (
                `url` varchar(255) NOT NULL,
                `site` varchar(255) NULL,
                `keyword` varchar(255) NULL,
                PRIMARY KEY (`url`)
                );'''.format(spider.name)
        self.cur.execute(sql)
        self.conn.commit()   # 在redis里设置关键词

    def process_item(self, item, spider):
        url = item.get("url")
        site = item.get("site")
        keyword = item.get("keyword")

        sql = '''insert ignore into {}(
                            url, site, keyword)
                    VALUES (%s, %s, %s)'''.format(spider.name)
        self.cur.execute(sql, (url, site, keyword))
        self.conn.commit()
        return item


class NewsSitePipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        self.cur = self.conn.cursor()

        sql = '''CREATE TABLE IF NOT EXISTS `job_news`.`{}`  (
                `title` varchar(255) NULL,
                `url` varchar(255) NOT NULL,
                `content` varchar(255) NULL,
                `date` timestamp(0) NULL,
                PRIMARY KEY (`url`)
                );'''.format(spider.name)
        self.cur.execute(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        url = item.get("url")
        title = item.get("title")
        content = item.get("content")
        date = item.get("date")

        sql = '''insert ignore into {}(
                            url, title, content, date)
                    VALUES (%s, %s, %s, %s)'''.format(spider.name)
        self.cur.execute(sql, (url, title, content, date))
        self.conn.commit()
        return item
