# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShixisengItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    money = scrapy.Field()
    place = scrapy.Field()
    education = scrapy.Field()
    week = scrapy.Field()
    month = scrapy.Field()
    lure = scrapy.Field()
    desc = scrapy.Field()
    company = scrapy.Field()
    people = scrapy.Field()



