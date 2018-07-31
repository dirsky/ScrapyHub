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

        #logging.CRITICAL - for critical errors (highest severity)
        #logging.ERROR - for regular errors
        #logging.WARNING - for warning messages
        #logging.INFO - for informational messages
        #logging.DEBUG - for debugging messages (lowest severity)

        #[e] DEBUG: Saved file log.txt
        self.log('Saved file %s' % filename)

        #下面是些处理这些站点的建议(tips):

            #使用user agent池，轮流选择之一来作为user agent。池中包含常见的浏览器的user agent(google一下一大堆)
            #禁止cookies(参考 COOKIES_ENABLED)，有些站点会使用cookies来发现爬虫的轨迹。
            #设置下载延迟(2或更高)。参考 DOWNLOAD_DELAY 设置。
            #如果可行，使用 Google cache 来爬取数据，而不是直接访问站点。
            #使用IP池。例如免费的 Tor项目 或付费服务(ProxyMesh)。
            #使用高度分布式的下载器(downloader)来绕过禁止(ban)，您就只需要专注分析处理页面。这样的例子有: Crawlera

        item = ExampleItem()
        item['Name'] = title
        item['Desc'] = title
        yield item

        print "----------parse  end ----------"

        