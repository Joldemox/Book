# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter


class BookPipeline(object):
    def open_spider(self, spider):
        self.file = open('book.json', 'wb')
        self.writer = JsonItemExporter(self.file)
        self.writer.start_exporting()

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item
