# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from db import database
import logging
from scrapy.exceptions import DropItem
class E04Pipeline:
    def process_item(self, item, spider):
        db = database()
        result = db.insert(item)
        if not result:
            raise DropItem("%s is duplicated"%item['name'])
        return item
