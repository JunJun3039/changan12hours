# -*- coding: utf-8 -*-
import scrapy
import time
import random
from douban.items import DoubanItem


class ShortSpider(scrapy.Spider):
    name = 'short'
    allow_domains = ['movie.douban.com']

    def start_requests(self):
        '''
        重写start_requests方法
        '''

        # 浏览器用户代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
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
            'https://movie.douban.com/subject/26849758/comments?start=0&limit=20&sort=new_score&status=P'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        '''
        获取下一页链接
        '''
        k = 0
        p = 1
        # 豆瓣只开放500条评论
        while k <= 480:
            url = 'https://movie.douban.com/subject/26849758/comments?start=' + str(k) + '&limit=20&sort=new_score&status=P'
            print('正在爬取第%d页数据' % p)
            p += 1
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.content_parse)
            k += 20
            time.sleep(round(random.uniform(2, 3), 2))

    def content_parse(self, response):
        '''
        获取用户评论信息
        '''
        contents = response.xpath('//div[@class="comment"]')
        for content in contents:
            item = DoubanItem()
            name = content.xpath('./h3/span[@class="comment-info"]/a/text()').extract()[0]
            score = content.xpath('./h3/span[@class="comment-info"]/span[2]').attrib.get('title')
            # 这里span标签内的文字换行会导致写入数据出现问题，因此直接把评论带标签拿出来，之后再做处理
            comment = content.xpath('./p/span[@class="short"]').extract()[0]
            date = content.xpath('./h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').extract()[0].strip()
            # 获取评论用户主页链接，用于爬取用户常居城市
            href = content.xpath('./h3/span[@class="comment-info"]/a/@href').extract()[0]
            item['name'] = name
            # 判断用户是否评分，未评分第二个span标签是时间，这里通过长度判断
            if len(score) < 5:
                item['score'] = score
            else:
                item['score'] = '--'
            item['comment'] = comment
            item['date'] = date
            item['href'] = href
            yield item # 返回item