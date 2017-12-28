# -*- coding: utf-8 -*-
import scrapy
from jingdongwang.items import JingdongwangItem1,JingdongwangItem2


class JingdongSpider(scrapy.Spider):
    headers={
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip,deflate,sdch, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cache-control':'max-age=0',
        'upgrade-insecure-requests':'1'}
    cookies={
        'user-key':'778d01ee-02e1-4c02-9d5d-49222b11a556',
        'ipLocation':'%u5e7f%u4e1c',
        'ipLoc-djd':'19-1705-19992-20008.138673371',
        'TrackID':'1IkTEHDzuwHFNOVs7N0LwXTj-BXI1c2nw0P53NnQIzWE1vQmCxL5zMUOgb_LROdlNMXyI1fpyxuVpgsI9D-Yn4A',
        'pinId':'bizS1gNJ6Rj1SHgKB1EQnw',
        'pin':'suwenkun1126',
        'unick':'suwenkun1126',
        ' _tp':'2a8Alm4EMNgaUjZZnaWaAw%3D%3D',
        '_pst':'suwenkun1126',
        'unpl':'V2_ZzNtbRdWFhNxXEZXextfA2JXEwoRBEAQdABPU3xNWVBkCkcNclRCFXMUR1xnGV4UZgIZXEpcQRVFCHZUehhdBGYBFV5GZwFLI1YCCDApbAZnMxptQlJLHXIOTlR6Hl0GZwMbW0tSQxJ9DUJkSx5sNVcCIlxyVnNeGwkLVH4RVAJhCxJcRVZAFXUBQF1%2bGVsNYgciXHJU',
        '__jdv':'122270672|123.sogou.com|t_1000003625_sogoumz|tuiguang|d0d75e1213274e0fbb2409866e4d28da|1505233578149',
        'cn':'0',
        'mt_xid':'V2_52007VwMXWlVfVFIfSB5dBmcDG1RUXVJdF0wdbFJmBkFaW15bRk9MGA4ZYlMWBkELAlofVRlcA24FE1BYWlRZFnkaXQVhHxNaQVhXSx9NEl8FbAARYl9oUmofSxleBmIDE1JtWFdcGA%3D%3D',
        '__jda':'122270672.14996791060211878416945.1499679106.1505373876.1505378735.14',
        ' __jdc':'122270672',
        '3AB9D23F7A4B3C9B':'YYLZ7AJ4ELY5PHQAUTPNP35LMZVWOXDL3PX2FHBB6J6V7N7RVG3AWUOX5LMWC2HSLNIVZKR4PAU57WEVSW2B5NETHQ',
        '__jdu':'14996791060211878416945'
    }

    name = 'jingdong'
    # allowed_domains = ['jd.com']
    def start_requests(self):
        for i in range(1,101):
            url='https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page='+str(2*i-1)+'&s=1&click=0'
            yield scrapy.Request(url=url,meta={'i':i},callback=self.parse)

    def parse(self, response):
        i=response.meta.get('i')
        print('=====================开始处理页面:#{}====================='.format(i))
        ids=set()
        item1=JingdongwangItem1()
        results=response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for result in results:
            id=result.xpath('./@data-pid').extract_first()
            if id:
                ids.add(id)
            item1['price']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract_first(default='Not Found')
            item1['title']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@title').extract_first(default='Not Found')
            item1['comment']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a/text()').extract_first(default='Not Found')
            item1['shop']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-shop"]/span[@class="J_im_icon"]/a/@title').extract_first(default='Not Found')
            yield item1
        url='https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page='+str(2*i)+'&show_items={}'.format(','.join(ids))
        yield scrapy.Request(url=url,headers=self.headers,cookies=self.cookies,callback=self.parse_other)

    def parse_other(self,response):
        item2=JingdongwangItem2()
        results=response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for result in results:
            item2['price']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract_first(default='Not Found')
            item2['title']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@title').extract_first(default='Not Found')
            item2['comment']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a/text()').extract_first(default='Not Found')
            item2['shop']=result.xpath('div[@class="gl-i-wrap"]/div[@class="p-shop"]/span[@class="J_im_icon"]/a/@title').extract_first(default='Not Found')
            yield item2





