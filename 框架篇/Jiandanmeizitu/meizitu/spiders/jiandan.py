# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem

class JiandanSpider(scrapy.Spider):
    name = 'jiandan'
    start_urls = ['http://jandan.net/ooxx/page-{}'.format(i) for i in range(1,146)]

    def parse(self, response):
        item=MeizituItem()
        image_urls=response.css('.commentlist li .row .text p img::attr(src)').extract()
        item['image_urls']=[('http:'+i)for i in image_urls]
        yield item


