# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GuokeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    focus=scrapy.Field()
    answer=scrapy.Field()
    title=scrapy.Field()
    link=scrapy.Field()
    summary=scrapy.Field()
    tags=scrapy.Field()


