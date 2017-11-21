# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    number = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    time = scrapy.Field()
    duty = scrapy.Field()
    require = scrapy.Field()

