# -*- coding: utf-8 -*-
import scrapy
from Douban.items import *


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 查找电影列表
        movies_list = response.xpath('//div[@class="info"]')
        print(len(movies_list))
        # 遍历列表
        for movie in movies_list:
            # 构建item
            item = DoubanItem()
            # 查找列表各项信息
            item['title'] = movie.xpath('./div[1]/a/span[1]/text()').extract()[0]
            item['rating_num'] = movie.xpath('./div[2]/div/span[2]/text()').extract()[0]
            item['info'] = ''.join(movie.xpath('./div[2]/p/text()').extract()).replace('\n', '').replace(' ', '').replace('\xa0', '').replace('\xee', '').replace('\xf6', '')
            item['quote'] = movie.xpath('./div[2]/p[2]/span/text()').extract_first()
            # print(item)
            yield item  # 返回列表
        # 翻页
        try:
            next_url = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()[0]
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url, callback=self.parse)
        except:
            pass