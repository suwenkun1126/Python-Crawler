# -*- coding: utf-8 -*-
import scrapy
from shixiseng.items import ShixisengItem


class ShixiSpider(scrapy.Spider):
    name = 'shixi'
    allowed_domains = ['shixiseng.com']
    start_urls = ['http://www.shixiseng.com/interns?p={}'.format(i)for i in range(1,501)]
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }

    def parse(self, response):
        links=response.css('.list .po-name .names.cutom_font')
        for link in links:
            link=response.urljoin(link.css('a::attr(href)').extract_first())
            yield scrapy.Request(link,headers=self.headers,meta={'detail_url':link},callback=self.parse_detail)

    def parse_detail(self,response):
        item=ShixisengItem()
        item['link']=response.meta['detail_url']
        item['name']=response.css('.new_job_name::text').extract_first()
        item['money']=response.css('.job_money.cutom_font::text').extract_first()
        item['place']=response.css('.job_position::text').extract_first()
        item['education']=response.css('.job_academic::text').extract_first()
        item['week']=response.css('.job_week.cutom_font::text').extract_first()
        item['month']=response.css('.job_time.cutom_font::text').extract_first()
        item['lure']=response.css('.job_good::text').extract_first()
        item['desc']=response.css('.job_detail::text').extract_first()
        item['company']=response.css('.job_com_name.cutom_font::text').extract_first()
        item['people']=response.css('.job_detail.job_detail_msg span::text').extract()[1]
        yield item




