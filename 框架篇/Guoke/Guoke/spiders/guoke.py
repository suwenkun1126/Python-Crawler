# -*- coding: utf-8 -*-
import scrapy
from Guoke.items import GuokeItem


class GuokeSpider(scrapy.Spider):
    name = 'guoke'
    allowed_domains = ['guokr.com']
    start_urls = ['http://www.guokr.com/ask/highlight/?page={}'.format(i)for i in range(1,101)]

    def parse(self, response):
        for result in response.css('.ask-list-cp li'):
            item = GuokeItem()
            item['focus']=result.css('.ask-focus-nums .num::text').extract_first()
            item['answer']=result.css('.ask-answer-nums .num::text').extract_first()
            item['title']=result.css('.ask-list-detials h2 a::text').extract_first()
            item['link']=result.css('.ask-list-detials h2 a::attr(href)').extract_first()
            item['summary']=result.css('.ask-list-summary::text').extract_first().strip()
            item['tags']=result.css('.tag::text').extract()
            yield item

