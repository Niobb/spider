# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    rating_num = scrapy.Field()
    info = scrapy.Field()
    quote = scrapy.Field()
