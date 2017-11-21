# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from Douban.settings import MONGODB_SETTINT
import pymongo

class Douban250Pipeline(object):
    def __init__(self):
        self.file = open('douban250.json', 'wb')


    def process_item(self, item, spider):
        item_dict = dict(item)
        item_json = json.dumps(item_dict, ensure_ascii=False) + ',\n'
        self.file.write(item_json.encode())
        return item

    def __del__(self):
        self.file.close()

class MongodbPipeline(object):
    # 写入数据库中
    def __init__(self):
        host = MONGODB_SETTINT['HOST']
        port = MONGODB_SETTINT['PORT']
        dbname = MONGODB_SETTINT['DBNAME']
        colname = MONGODB_SETTINT['COLNAME']
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[dbname]
        self.col = self.db[colname]

    def process_item(self, item, spider):
        self.col.insert(dict(item))
        return item

    def __del__(self):
        self.client.close()