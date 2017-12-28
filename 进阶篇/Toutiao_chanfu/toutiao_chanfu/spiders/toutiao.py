# -*- coding: utf-8 -*-
import scrapy
import json
from toutiao_chanfu.items import ToutiaoChanfuItem


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    start_urls = ['https://ic.snssdk.com/article/v2/tab_comments/?resolution=640*960&aggr_type=1&count=20&group_id=6462587303142359566&item_id=6462587303142359566&offset={}'.format(i*20) for i in range(0,76)]

    def parse(self, response):
        item=ToutiaoChanfuItem()
        html=response.text
        if html:
            content=json.loads(html)
            if content:
                datas=content.get("data")
                if datas:
                    for data in datas:
                        comment=data.get("comment")
                        if comment:
                            item['user_name']=comment.get("user_name")
                            item['text']=comment.get("text")
                            # print(item['user_name']+':'+item['text']+'\n')
                            yield item

