# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class DoubanPipeline(object):
    def __init__(self):
        self.cli=pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db=self.cli['douban']
        self.coll=self.db['ds2']
    def process_item(self, item, spider):
        ite=dict(item)
        self.coll.insert(ite)
        return item




