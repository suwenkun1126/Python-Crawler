# -*- coding: utf-8 -*-
import scrapy
from Taonvlang.items import TaonvlangItem
from bs4 import BeautifulSoup
import re
import json

class TaobaoSpider(scrapy.Spider):
    Num=1
    name = 'taobao'
    # allowed_domains = ['www.taobao.com']

    def start_requests(self):
        urls=['https://mm.taobao.com/json/request_top_list.htm?page={}'.format(i) for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_user_id)

    def parse_user_id(self, response):
        urls=response.css('.list-item .personal-info .pic-word .top a::attr(href)').extract()
        user_ids=[url.split('=')[-1] for url in urls if url]
        for user_id in user_ids:
            url='https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20={}&page=1'.format(user_id)
            yield scrapy.Request(url,meta={'user_id':user_id},callback=self.parse_album_id)

    def parse_album_id(self, response):
        user_id=response.meta.get('user_id')
        if response.status==200:
            html=response.text
            soup=BeautifulSoup(html,'lxml')
            results=soup.select('.mm-photo-list.clearfix .mm-photo-cell')
            for result in results:
                link=result.select('.mm-photo-cell-middle h4 a')[0]['href']
                album_id=re.search('album_id=(.*?)&',link).group(1)
                page_content=result.select('.mm-photo-cell-middle .mm-pic-number')[0].text
                pages=int(re.findall('\d+',page_content)[0])
                for page in range(1,int(pages/16)+2):
                    print('开始处理用户:{},相册编号:{},第{}页,#{}'.format(user_id,album_id,page,self.Num))
                    self.Num=self.Num+1
                    url='https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id='+str(user_id)+'&album_id='+str(album_id)+'&page='+str(page)
                    yield scrapy.Request(url,callback=self.parse)

    def parse(self,response):
        item=TaonvlangItem()
        html=response.text
        contents=json.loads(html)
        piclists=contents.get('picList')
        for piclist in piclists:
            item['user_id'] = piclist.get('userId')
            item['album_id'] = piclist.get('albumId')
            item['title']=piclist.get('des')
            item['picurl']='http:'+piclist.get('picUrl').replace('_290x10000','_620x10000')
            yield item







