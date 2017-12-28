# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class DianpingItem(Item):
    # define the fields for your item here like:
    name=Field()        #昵称
    img_url=Field()     #头像地址

    comment=Field()     #点评
    save=Field()        #收藏
    sign=Field()        #签到
    photo=Field()       #图片
    list=Field()        #榜单
    topic=Field()       #帖子

    focus=Field()       #关注
    fan=Field()         #粉丝
    interact=Field()    #互动
    contribute=Field()  #贡献值
    level=Field()       #社区等级
    sign_time=Field()   #注册时间

    marry=Field()       #恋爱状况
    birth=Field()       #生日
    star=Field()        #星座

