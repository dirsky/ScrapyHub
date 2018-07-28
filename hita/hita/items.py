# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HitaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    DE_Name = scrapy.Field()
    DE_Flag = scrapy.Field()
    DE_Desc = scrapy.Field()
    DE_Type = scrapy.Field()
    DE_Format = scrapy.Field()
    DE_Allow = scrapy.Field()
