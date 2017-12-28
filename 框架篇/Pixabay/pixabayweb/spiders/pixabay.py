# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from pixabayweb.items import PixabaywebItem

class PixabaySpider(scrapy.Spider):
    name = 'pixabay'
    start_urls=['https://pixabay.com/zh/photos/?q=beauty&pagi={}'.format(i)for i in range(1,414)]

    def parse(self, response):
        base_url='https://pixabay.com'
        links=response.xpath('//div[@class="flex_grid credits"]/div[@class="item"]')
        for link in links:
            url=base_url+link.xpath('./a/@href').extract_first()
            yield Request(url=url,callback=self.parse_detail)

    def parse_detail(self,response):
        item=PixabaywebItem()
        item['image_urls']=response.xpath('//*[@id="media_container"]/img/@src').extract_first()
        yield item



