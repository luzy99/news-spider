# news_spider
关键词式指定站点新闻爬虫
## 介绍
- 基于Scrapy框架
- 谷歌高级搜索（爬取新闻链接）
- 关键词、站点自定义
- 新闻页面解析（已包含人民日报、纽约时报、东方新闻、星岛新闻页面解析）
- MySQL存储
- 可拓展
## 目录结构
- 主体为Scrapy工程目录结构
- `utils`目录下包括繁简转换插件，[原项目地址](https://github.com/skydark/nstools/tree/master/zhtools)
- `analysis`目录下为一些简单的数据分析代码，包括分词、词频统计等。
- `spiders`下包括谷歌搜索、人民日报、纽约时报、东方新闻、星岛新闻爬虫

## 如何使用

1. 修改`settings.py`中关于数据库的配置项

    ```python
    MYSQL_HOST = '127.0.0.1'	# 数据库地址
    MYSQL_DBNAME = 'job_news'	# 数据库名称
    MYSQL_USER = 'root'  # 数据库账号
    MYSQL_PASSWD = '123456'	# 数据库密码
    MYSQL_PORT = 3306
    ```

2. 启动谷歌搜索爬虫

   ```sh
   scrapy crawl google -a kw=xxx -a site=xxx
   ```

3. 启动新闻站点爬虫

    ```
    scrapy crawl 爬虫名
    ```

## demo展示

- 新闻目录

![新闻目录](https://cdn.jsdelivr.net/gh/luzy99/cdn@latest/img/20200919223503.png)

- 新闻内容

![新闻内容](https://cdn.jsdelivr.net/gh/luzy99/cdn@latest/img/20200919223524.png)

- 词云

![词云](https://cdn.jsdelivr.net/gh/luzy99/cdn@latest/img/20200919223725.png)

- 词频

![词频](https://cdn.jsdelivr.net/gh/luzy99/cdn@latest/img/20200919223810.png)

