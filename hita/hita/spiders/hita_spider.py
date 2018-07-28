# -*- coding: utf-8 -*-
import scrapy
#from hita.items import HitaItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "hita"
    allowed_domains = ["omaha.org.cn"]
    start_urls = [
        "http://meta.omaha.org.cn/dataElement/element"
    ]

    def parse(self, response):
        #filename = response.url
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

        print response.xpath('//title/text()').extract_first()
        print "------------------start-----------------------"

        url_parts = response.url.split("/")
        home_url = url_parts[0] + "//" + url_parts[2]
        print home_url

        for li in response.css('ul#mainCatalog li'):
            #item = HitaItem()
            title = li.css('a::text').extract_first()
            print title
            #item['DE_Name'] = title

            link = home_url + li.xpath('a/@href').extract_first()
            print link
            
            with open("urls.txt","a") as f:
                f.write(link + "\n") 
            
            #yield item


        print "-------------------end------------------------"