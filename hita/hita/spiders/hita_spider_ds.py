# -*- coding: utf-8 -*-
import scrapy
from hita.items import HitaItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "ds"
    allowed_domains = ["omaha.org.cn"]

    start_urls = [
        "http://meta.omaha.org.cn/dataSet/"
    ]

    home_url = 'http://meta.omaha.org.cn/'


    def parse(self, response):
        print response.xpath('//title/text()').extract_first()
        print "------------------start-----------------------"

        pageNo = response.css('ul.page li')[-2].css('a::text').extract_first()
        print "共有" + pageNo + "页"

        for i in range(1, int(pageNo)+1):
            url = response.url + "?&pageNo=" + str(i)
            yield scrapy.Request(url=url,callback=self.parse_detail)

        print "----------------end--------------------"


    def parse_detail(self, response):
        print "-------------parse_detail---------------"
        print response.url

        urls = ''
        #/html/body/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/a
        for li in response.css('tbody > tr'):
            href = li.xpath('td[2]/a/@href').extract_first().strip().replace(' ','')
            href = self.home_url + href + '\n'
            urls += href
        
        self.write2txt(urls)
        
        print "-----------parse_detail end-------------"
    

    def write2txt(self, urls):
        filename = 'DS/Urls.txt'
        with open(filename,"a") as f:
            f.write(urls) 