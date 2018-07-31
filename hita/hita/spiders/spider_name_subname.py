# -*- coding: utf-8 -*-
import scrapy
from hita.items import ExampleItem

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "e"
    allowed_domains = ["omaha.org.cn"]
    home_url = "http://meta.omaha.org.cn"

    def start_requests(self):
        urls = []

        urls.append('http://meta.omaha.org.cn/dataSet')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        title = response.xpath('//title/text()').extract_first()
        print title
        print response.url
        print "----------parse start----------"
        
        item = ExampleItem()
        item['Name'] = title
        item['Desc'] = title
        yield item

        print "----------parse  end ----------"

        