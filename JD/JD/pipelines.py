# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class JdPipeline(object):
    def __init__(self):
        self.file = open('book.csv', 'wb')

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(item_json.encode())
        return item

    def __del__(self):
        self.file.close()
