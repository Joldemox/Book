# -*- coding: utf-8 -*-
import scrapy
from Book.items import BookItem
import json
from copy import deepcopy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    # 测试翻页代码
    page = 0

    # 解析分类标签
    def parse(self, response):
        # 2、图书分类标签
        # dt_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt')
        dt_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt[1]')
        # 3、图书分类，获取名字与链接
        # 遍历所有dt标签，使用xpath中的follwong - sibling::*[1]
        # 取出下一届点的平级元素dd
        for dt in dt_list:
            item = BookItem()
            item['big_name'] = dt.xpath('a/text()').extract_first()
            # 具体分类
            em_list = dt.xpath('./following-sibling::*[1]/em')
            for em in em_list[:1]:
                item['small_name'] = em.xpath('a/text()').extract_first()
                # 拼接url前缀
                small_link = 'https:' + em.xpath('a/@href').extract_first()

                # 发送图书列表页（第二层）
                yield scrapy.Request(small_link, callback=self.parse_book, meta={'book': deepcopy(item)})

    # 解析列表页的图书
    def parse_book(self, response):
        # 从上一级接受tiem
        item = response.meta['book']
        # 取出所有图书book_list
        book_list = response.xpath('//*[@id="plist"]/ul/li')
        # 测试数据
        # for book in book_list:
        for book in book_list[:1]:
            # 图片
            item['book_img_url'] = 'https:' + book.xpath('.//div[@class="p-img"]/a/img/@src').extract_first()
            # 名字
            item['book_name'] = book.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            # 作者
            item['book_author'] = book.xpath('.//span[@class="author_type_1"]/a/text()').extract_first()
            # 出版社
            item['book_store'] = book.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
            # 出版时间
            item['book_time'] = book.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()
            # 价格
            # item['book_price'] = book.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            # 取出具体图书的ID
            book_id = book.xpath('./div/@data-sku').extract_first()
            price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(book_id)
            # 发送价格请求
            yield scrapy.Request(price_url, callback=self.parse_price, meta={'book': deepcopy(item)})

            # yield item

        # 值做前5的翻页
        self.page += 1
        if self.page > 4:
            return

        # 列表翻页
        # 1、取出'下一页'标签的url
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        # 2、发送下一页请求
        yield response.follow(
            # 会自动拼接url进行请求
            next_url,
            callback=self.parse_book,
            meta={'book': item},
        )
        # 3、判断结束，如果next_url为none，就表示结束

    # 解析价格
    def parse_price(self, response):
        item = response.meta['book']
        item['book_price'] = json.loads(response.body.decode())[0]['p']
        yield item
