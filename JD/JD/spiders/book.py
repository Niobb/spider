# -*- coding: utf-8 -*-
import scrapy
from JD.items import *
import json
import re
from scrapy_redis.spiders import RedisSpider

class BookSpider(RedisSpider):
    name = 'book'
    redis_key = 'jdbook'

    def __init__(self, *args, **kwargs):
        # domain = kwargs.pop('domain', '')
        self.allowed_domains = ['jd.com','3.cn']
        super(BookSpider, self).__init__(*args, **kwargs)

    # start_urls = ['http://book.jd.com/booksort.html']

    def parse(self, response):
        # 获取大分类列表
        big_cate_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt')
        print(len(big_cate_list))
        # 遍历
        for big_cate in big_cate_list:
            big = {}
            # 大分类和大分类的url
            big['big_cate'] = big_cate.xpath('./a/text()').extract()[0]
            big['big_cate_url'] = 'http:' + big_cate.xpath('./a/@href').extract()[0]
            # 小分类列表
            small_cate_list = big_cate.xpath('./following-sibling::dd[1]/em')
            # 遍历
            for small_cate in small_cate_list:
                # 小分类和小分类url
                small = {}
                small['big_cate'] = big['big_cate']
                small['big_cate_url'] = big['big_cate_url']
                small['small_cate'] = small_cate.xpath('./a/text()').extract_first()
                small['small_cate_url'] = 'http:' + small_cate.xpath('./a/@href').extract_first()
                yield scrapy.Request(
                    small['small_cate_url'],
                    callback=self.parse_list,
                    meta={"meta_1":small}
                )

    def parse_list(self, response):
        temp = response.meta['meta_1']
        # 获取列表页的图书列表
        book_list = response.xpath('//*[@id="plist"]/ul/li')
        print(len(book_list))
        # # 遍历
        for book in book_list:
            books = {}
            books.update(temp)
            books['book_name'] = book.xpath('./div/div[3]/a/em/text()|./div/div/div[2]/div[1]/div[3]/a/em/text()').extract_first().strip()
            books['detail_url'] = 'http:' + book.xpath('./div/div[1]/a/@href|./div/div/div[2]/div[2]/div[1]/a/@href').extract_first()
            books['publisher'] = book.xpath('./div/div[4]/span[2]/a/text()|./div/div/div[2]/div[1]/div[4]/span[2]/a/text()').extract_first()
            books['pub_time'] = book.xpath('./div/div[4]/span[3]/text()|./div/div/div[2]/div[1]/div[4]/span[3]/text()').extract_first().strip()
            url = books['detail_url']
            # print('+++', books)
            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                meta={'meta_2': books}
            )

        # 翻页
        try:
            next_page = 'http://list.jd.com' + response.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract_first()
            yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass

    def parse_detail(self, response):
        temp = response.meta['meta_2']
        # print(item)
        item = JdItem()
        item.update(temp)
        # print('------', response.url)
        item['cover_url'] = 'http:' + response.xpath('//*[@id="spec-n1"]/img/@src').extract_first()
        item['authors'] = ' '.join(response.xpath('//*[@id="p-author"]/a/text()').extract())
        r = re.compile('jd.com/(\d+).html',re.S)
        item['skuid'] = r.findall(response.url)[0]
        print(item['skuid'])
        # item['skuid'] = response.xpath('//*[@id="parameter2"]/li[4]/text()').extract_first().strip().split('：')[-1]
        url = 'https://p.3.cn/prices/mgets?pduid=1504858781822797570775&skuIds=J_' + item['skuid']
        print(url)
        # print(item)
        yield scrapy.Request(url, callback=self.parse_price, meta={'meta_3':item})
        # item['content'] = response.xpath('//*[@id="detail-tag-id-3"]/div[2]/div/p/text()|//*[@id="detail-tag-id-3"]/div[2]/div/text()').extract()
        # item['authors_info'] = ''.join(response.xpath('//*[@id="detail-tag-id-4"]/div[2]/div/text()|//*[@id="detail-tag-id-4"]/div[2]/div/p/text()').extract())

    def parse_price(self, response):
        # print('++++++++++++++++++++++++++')
        temp = response.meta['meta_3']
        item = JdItem()
        item.update(temp)
        try:
            item['price'] = json.loads(response.text)[0]['op']
        # print(item)
        except:
            item['price'] = 'null'
        yield item