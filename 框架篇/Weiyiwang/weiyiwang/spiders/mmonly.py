# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from weiyiwang.items import WeiyiwangItem

class MmonlySpider(scrapy.Spider):
    name = 'mmonly'
    allowed_domains = ['mmonly.cc']
    start_urls = ['http://www.mmonly.cc/gqbz/list_41_{}.html'.format(i) for i in range(1,293)]

    def parse(self, response):
        links=response.css('.item.masonry_brick.masonry-brick')
        for link in links:
            detail_url = link.css('.ABox a::attr(href)').extract_first()
            pages=link.css('.items_likes::text').re_first('共(.*)张')
            if pages==1:
                url=detail_url
                yield Request(url=url, callback=self.parse_detail)
            else:
                for i in range(1,int(pages)):
                    url=detail_url.split('.html')[0]+'_{}.html'.format(i)
                    yield Request(url=url,callback=self.parse_detail)

    def parse_detail(self,response):
        item=WeiyiwangItem()
        item['title']=response.css('.wrapper.clearfix.imgtitle h1::text').extract_first()
        item['img_url']=response.css('.big-pic a img::attr(src)').extract_first()
        yield item


