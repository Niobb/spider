# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import *
import re

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    def parse(self, response):
        node_list = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')
        print(len(node_list))
        for node in node_list:
            item = TencentItem()
            item['name'] = node.xpath('.//td[1]/a/text()').extract()[0]
            item['link'] = 'http://hr.tencent.com/' + node.xpath('.//td[1]/a/@href').extract()[0]
            item['number'] = node.xpath('.//td[3]/text()').extract()[0]
            item['address'] = node.xpath('.//td[4]/text()').extract()[0]
            try:
                item['type'] = node.xpath('.//td[2]/text()').extract()[0]
            except:
                item['type'] = 'null'
            item['time'] = node.xpath('.//td[5]/text()').extract()[0]
            # print(item)
            yield scrapy.Request(item['link'], callback=self.parse_detail, meta={'data': item})
        page = re.search(r'\d+',response.url).group(0)
        print('当前页数：%s' % (int(int(page)/10)+1))
        try:
            next_url = 'http://hr.tencent.com/' + response.xpath('//*[@id="next"]/@href').extract()[0]
            # print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
        except:
            pass

    def parse_detail(self, response):
        print(response.status)
        item = response.meta['data']
        item['duty'] = ' '.join(response.xpath('//tr[@class="c"][1]/td/ul/li/text()').extract())
        item['require'] = ' '.join(response.xpath('//tr[@class="c"][2]/td/ul/li/text()').extract())
        yield item

