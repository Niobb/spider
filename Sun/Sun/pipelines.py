# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DongguanPipeline(object):
    def __init__(self):
        self.file = open('dongguan.json', 'wb')

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(item_json.encode())
        return item

    def close_spider(self, response):
        self.file.close()