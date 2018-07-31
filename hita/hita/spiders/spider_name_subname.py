# -*- coding: utf-8 -*-
import scrapy
import logging
from hita.items import ExampleItem

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "e"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com",
    ]

    def start_requests(self):
        self.start_urls.append("http://www.qq.com")

        #格式化字符串
        s = 'ss{g}s'
        print s.format(g='k')

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        #[root] ERROR: ------------k----------
        logging.error('------------k----------')
        title = response.xpath('//title/text()').extract_first()
        print title
        print response.url
        #//div[@class="mine"]
        # @用来读取属性
        print response.xpath('//*[@id="su"]/@value').extract_first()
        print "----------parse start----------"
        filename = 'log.txt'

        #[e] DEBUG: Saved file log.txt
        self.log('Saved file %s' % filename)

        item = ExampleItem()
        item['Name'] = title
        item['Desc'] = title
        yield item

        print "----------parse  end ----------"

        