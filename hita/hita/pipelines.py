# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from hita.items import HitaItem
from hita.items import ExampleItem

class HitaPipeline(object):
    def process_item(self, item, spider):
        print('--------Pipeline-----------')
        print('--------Pipeline-----------')
        print('--------Pipeline-----------')
        print('--------Pipeline-----------')
        print(item['Name'])
        return item
