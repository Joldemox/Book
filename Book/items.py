# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 分类名称
    big_name = scrapy.Field()
    # 具体分类名称
    small_name = scrapy.Field()
    # 图片
    book_img_url = scrapy.Field()
    # 名字
    book_name = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 出版社
    book_store = scrapy.Field()
    # 出版时间
    book_time = scrapy.Field()
    # 价格
    book_price = scrapy.Field()
