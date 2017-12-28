# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapy.http.request import Request
from dianping.items import DianpingItem


class DianpingComSpider(scrapy.Spider):
    name = 'dianping.com'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/memberlist/star/1708/{}'.format(i) for i in range(0,26)]#15代表厦门

    def parse(self, response):
        urls=response.xpath('//ul[@class="uList"]/li')
        for url in urls:
            url='http://www.dianping.com'+url.xpath('a[@class="img"]/@href').extract_first()
            yield scrapy.Request(url=url,callback=self.parse_detail)

    def parse_detail(self,response):
        item=DianpingItem()
        item['name']=response.xpath('//h2[@class="name"]/text()').extract_first()
        item['img_url']=response.xpath('//div[@class="pic"]/a/img/@src').extract_first()

        item['comment']=response.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li[2]/a/text()').extract_first()[3:-1]
        item['save']=response.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li[3]/a/text()').extract_first()[3:-1]
        item['sign']=response.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li[4]/a/text()').extract_first()[3:-1]
        item['photo']=response.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li[5]/a/text()').extract_first()[3:-1]
        item['list']=response.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li[6]/a/text()').extract_first()[3:-1]
        item['topic']=response.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li[7]/a/text()').extract_first()[3:-1]

        item['focus']=response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[1]/a/strong/text()').extract_first()
        item['fan']=response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[2]/a/strong/text()').extract_first()
        item['interact']=response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[3]/a/strong/text()').extract_first()
        item['contribute']=response.xpath('//*[@id="J_col_exp"]/text()').extract_first()
        item['level']=response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/p[2]/text()').extract_first()
        item['sign_time']=response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/p[3]/text()').extract_first()

        item['marry']=response.xpath('//*[@id="J_UMoreInfoD"]/ul[1]/li[1]/text()').extract_first()
        item['birth']=response.xpath('//*[@id="J_UMoreInfoD"]/ul[1]/li[2]/text()').extract_first()
        item['star']=response.xpath('//*[@id="J_UMoreInfoD"]/ul[1]/li[3]/text()').extract_first()
        yield item





















