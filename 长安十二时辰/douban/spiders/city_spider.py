# -*- coding: utf-8 -*-
import scrapy
import time
import random
import pandas as pd
from douban.items import CityItem


class ShortSpider(scrapy.Spider):
    name = 'city'
    allow_domains = ['www.douban.com']

    def start_requests(self):
        '''
        重写start_requests方法
        '''

        # 浏览器用户代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        # 指定cookies
        self.cookies = {
            '__utma':'30149280.1521389037.1561303458.1561907041.1561962380.3',
            '__utma':'223695111.427576477.1561907116.1561907116.1561962381.2',
            '__utmb':'223695111.0.10.1561962381',
            '__utmb':'223695111.0.10.1561962381',
            '__utmc':'30149280',
            '__utmc':'223695111',
            '__utmv':'30149280.19358',
            '__utmz':'30149280.1561962380.3.3',
            '__utmz':'223695111.1561962381.2.2',
            '__yadk_uid':'eUXrzWGBRRqUqhWmGrkp6fzh9BO7wJlv',
            '_pk_id.100001.4cf6':'127bbb690bd4b89e',
            '_pk_ref.100001.4cf6	':'%5B%22%22%2C%22%22%2C1561962380%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2Fcrastal%2F%22%5D	',
            '_pk_ses.100001.4cf6	':'*',
            '_vwo_uuid_v2':'DFBF6B35B552339DEB2B7CC602D8E8209|288d16026d58b592ac5db9124500193e	',
            'ap_v':'0,6.0',
            'bid':'e73B5o4gSII',
            'ck	':'dW3-',
            'dbcl2':'"193583045:XOi/1Xb5EjM"',
            'll	':'"118285"',
            'push_doumail_num	':'0',
            'push_noty_num':'0'
        }
        urls = [
            'https://www.douban.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        '''
        获取下一页链接
        '''
        p = 1
        df = pd.read_csv('./comments.csv', names=['name', 'score', 'comments', 'date', 'href'])
        hrefs = df.href
        for href in hrefs:
            print('正在爬取第%d页数据' % p)
            p += 1
            yield scrapy.Request(url=href, headers=self.headers, cookies=self.cookies, callback=self.city_parse)
            time.sleep(round(random.uniform(2, 3), 2))

    def city_parse(self, response):
        '''
        获取用户评论信息
        '''
        item = CityItem()
        city = response.xpath('//div[@class="user-info"]/a/text()')
        # 有些用户没有填写居住城市
        if city:
            item['city'] = city.extract()[0]
        else:
            item['city'] = '--'
        yield item # 返回item