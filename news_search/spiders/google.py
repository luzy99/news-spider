# -*- coding: utf-8 -*-
import scrapy
import time
from bs4 import BeautifulSoup
from ..items import SearchResultItem


class GoogleSpider(scrapy.Spider):
    name = 'google'
    # allowed_domains = ['google.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'news_search.pipelines.GooglePipeline': 200,
        }
    }
    kw = ''  # 搜索关键词
    site = ''  # 搜索站点
    altUrl = 'soo.panda321.com'
    baseUrl = 'https://%s/search?q=site:{site}+{kw}&filter=0&num=100&sourceid=chrome' % altUrl
    page = 1

    # scrapy crawl google -a kw=xxx -a site=xxx
    #
    # site:
    #       cn.nytimes.com
    #       people.com.cn
    #       orientaldaily.on.cc
    #       singtaousa.com

    def __init__(self, kw=None, site=None, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        self.kw = kw
        self.site = site
        self.headers = {'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                        'cookie': 'CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; SID=0QduTWkC5WbWkRJ63wWb46mnkdSHarS9NMhaQmCnz58nNZnOYRR7LkQvoB-fe-DgpzUiRA.; __Secure-3PSID=0QduTWkC5WbWkRJ63wWb46mnkdSHarS9NMhaQmCnz58nNZnOK_M0BfqLD42lVqMX5sjbxw.; HSID=AdXC9rTUMuMNSvPwP; SSID=AD7gSXOTRqul8A2Kw; APISID=StBKOvTSy5IPWOGh/AHDpUXwm2sDTY3nfw; SAPISID=CdwCqMaPISDAnCob/A9sJfOvpQUKruqkK-; __Secure-3PAPISID=CdwCqMaPISDAnCob/A9sJfOvpQUKruqkK-; OTZ=5596630_24_24__24_; NID=204=eRK2dGvcN_QRHPPiKalXJWogWrmYN0S-9a2NU6_ToF9cQ_3VRA4_ssfOer1zASep-3M7ik-DcI0quqEQevEJEuT09dP6ODCF--55gs8YcBQa_5xjbsyHVBCMw5v47IHOEyCaImP0zwSuhJRJJbf0GMuWkqRSWh1ci4SU3MBe55puHucFINQteFNsrYHvgDqxDTbArdPrL0_7sajw3SVCF6QWDGkmED19V0sDzF-hE0kRjgRGdqFLtRxDoWhhKkca0oMsjB_6mLFaZrh4CLdojIY4UKEtwIpRBwGi6LSfiRR9K3SGBZBNDW36Fa0zRmFuGw190wxW6LJVNZ_M4qLX2IEiiVnJe0HTRSY6tZKEYySlvMxghlJt; 1P_JAR=2020-09-01-13; DV=M2atO2b0mIsWYPXf0FOdhZCXKpCdRBc; SIDCC=AJi4QfG8spkcI2-4aGxI_PwiJt7kIzsBwMgZGNavWpEws5NQHslcvZFKMHEA5wTbhkeSRQE4yXkU; __Secure-3PSIDCC=AJi4QfH2M-p7w1F0sPOT7QBYiEai6YE2cNq7cIV_DXVePrboFrsISRP7nfcfkEZVsZUv5CE4XAc'}

    def start_requests(self):
        url = self.baseUrl.format(site=self.site, kw=self.kw)

        yield scrapy.Request(url, callback=self.parse, dont_filter=True, headers=self.headers)

    def parse(self, response):
        item = SearchResultItem()
        # 获取链接
        soup = BeautifulSoup(response.body, 'lxml')

        contents = soup.select('.r > a')

        for tag in contents:
            if 'paper.people.com.cn' in tag['href']:
                continue
            item['url'] = tag['href']
            if self.site == 'cn.nytimes.com':
                item['url'] = self.nytimes_process(item['url'])
            item['site'] = self.site
            item['keyword'] = self.kw
            yield item

        # 搜索下一页
        pageNext = soup.select('#pnnext')
        if len(pageNext) != 0:
            nextUrl = pageNext[0]['href']
            if nextUrl is not None:
                nextUrl = response.urljoin(nextUrl)
                # print(nextUrl)
                time.sleep(5)
                self.page += 1
                print('【page %d】' % self.page)
                yield scrapy.Request(nextUrl, callback=self.parse, dont_filter=True, headers=self.headers)

    def nytimes_process(self, url):
        return url.replace("en-us/", "").replace("dual/", "").replace("zh-hant/", "")
