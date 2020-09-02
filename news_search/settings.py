# -*- coding: utf-8 -*-
import random
# Scrapy settings for news_search project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'news_search'

SPIDER_MODULES = ['news_search.spiders']
NEWSPIDER_MODULE = 'news_search.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news_search (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

COOKIES_ENABLED = True

# user agent 列表
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
]
# 随机生成user agent
USER_AGENT = random.choice(USER_AGENT_LIST)

# MySQL配置
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'job_news'
MYSQL_USER = 'root'  # 数据库账号，请修改
MYSQL_PASSWD = '123456'
MYSQL_PORT = 3306

DOWNLOAD_DELAY = 4