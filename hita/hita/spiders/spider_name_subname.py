# -*- coding: utf-8 -*-
import scrapy
import logging
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

        #格式化字符串
        s = 'ss{g}s'
        print s.format(g='k')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        #[root] ERROR: ------------k----------
        logging.error('------------k----------')
        title = response.xpath('//title/text()').extract_first()
        print title
        print response.url
        print "----------parse start----------"
        filename = 'log.txt'

        #[e] DEBUG: Saved file log.txt
        self.log('Saved file %s' % filename)

        item = ExampleItem()
        item['Name'] = title
        item['Desc'] = title
        yield item

        print "----------parse  end ----------"

        