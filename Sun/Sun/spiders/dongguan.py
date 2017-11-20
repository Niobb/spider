# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Sun.items import *
from scrapy_redis.spiders import RedisCrawlSpider

class DongguanSpider(RedisCrawlSpider):
    name = 'dongguan'
    redis_key = 'sun0769'
    # allowed_domains = ['sun0769.com']
    # start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4']

    rules = (
        # 构建列表url的提取规则
        Rule(LinkExtractor(allow=r'sun0769.com/index.php/question/questionType'),callback='parse_page', follow=True),
        # 构建detail页的提取规则
        Rule(LinkExtractor(allow=r'sun0769.com/html/question/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print(response.url)
        item = DongguanItem()
        item['number'] = response.xpath('//div[@class="pagecenter p3"]/div/div/div/strong/text()').extract()[0].split(':')[-1].replace('\xa0', '')
        item['title'] = response.xpath('//div[@class="pagecenter p3"]/div/div/div/strong/text()').extract()[0].split('：')[1].split('\xa0')[0]
        item['url'] = response.url
        item['content'] = ' '.join(response.xpath('//div[@class="c1 text14_2"]/text()|//div[@class="c1 text14_2"]/div[@class="contentext"]/text()').extract()).replace('\xa0', '').replace(' ', '').replace('\t', '')
        # print(item)
        yield item

    def parse_page(self, response):
        url = response.url
        try:
            page = int(str(url).split('page=')[-1])
        except:
            page = 0
        print('当前页数为：%s' % ((page/30)+1))