# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HexunpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()#文章名
    url=scrapy.Field()#文章链接
    hits=scrapy.Field()#文章点击数
    comment=scrapy.Field()#文章评论数
    

