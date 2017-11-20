# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    '''
    书名，大分类，小分类，封面图片链接，详情页面url，
    作者，出版社，出版时间，价格，大分类页面ur，小分类页面urll
    '''
    book_name = scrapy.Field()

    big_cate = scrapy.Field()
    big_cate_url = scrapy.Field()

    small_cate = scrapy.Field()
    small_cate_url = scrapy.Field()

    cover_url = scrapy.Field()
    detail_url = scrapy.Field()

    authors = scrapy.Field()
    publisher = scrapy.Field()
    pub_time = scrapy.Field()

    price = scrapy.Field()
    skuid = scrapy.Field()
    # content = scrapy.Field()
    # authors_info = scrapy.Field()






