# -*- coding: utf-8 -*-
import scrapy
from hita.items import HitaItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "h2"
    allowed_domains = ["omaha.org.cn"]
    stop_time = 0
    home_url = "http://meta.omaha.org.cn"

    def start_requests(self):
        urls = []

        #从word中获取需要查询的单词
        word_file = open('./urls.txt', 'r')
        for one in word_file:
            one = one.replace('\r','').replace('\n','')
            print one
            urls.append(one)            
        word_file.close()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #filename = response.url
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

        print response.xpath('//title/text()').extract_first()
        print "------------------start-----------------------"
        
        #http://meta.omaha.org.cn/range/?catalogCode=CV02.01&pageNo=1
        #抓取页码
        pageNo = response.css('ul.page li')[-2].css('a::text').extract_first()
        print "共有" + pageNo + "页"
        for i in range(1, int(pageNo)+1):
            url = ""
            url = response.url + "&pageNo=" + str(i)
            print url
            yield scrapy.Request(url=url,callback=self.parse_detail)

        print "----------------end--------------------"


    def parse_detail(self, response):
        print "-------------parse_detail---------------"
        #print response.xpath('//title/text()').extract_first()
        url_part = response.url.split('&')
        FileName = url_part[0][-7:]
        print FileName
        #print response.url

        with open(FileName + ".txt","a") as f:
            for li in response.css('tbody > tr'):
                href = li.xpath('td[2]/a/@href').extract_first().strip().replace(' ','')
                url = self.home_url + href
                print url
                f.write(url + "\n") 
                yield scrapy.Request(url=url,callback=self.parse_foot)
        
        print "-----------parse_detail end-------------"


    def parse_foot(self, response):
        print "-------------parse_foot---------------"
        print response.xpath('//title/text()').extract_first()
        print response.url
        url_part = response.url.split('=')
        FileName = url_part[1][0:7]
        print FileName
        print "------head end------"
        #tb = '/html/body/div[2]/div[1]/div[2]/table'
        #print response.xpath(tb + '/tr[4]/td[3]/text()' ).extract_first()
        #print response.xpath(tb + '/tr[5]/td[3]/text()' ).extract_first()
        #print response.xpath(tb + '/tr[10]/td[3]/text()').extract_first()
        #print response.xpath(tb + '/tr[14]/td[3]/text()').extract_first()
        #print response.xpath(tb + '/tr[15]/td[3]/text()').extract_first()
        #print response.xpath(tb + '/tr[16]/td[3]/text()').extract_first()

        with open( "DE_detail.txt","a") as f:
            tb = '/html/body/div[2]/div[1]/div[2]/table'
            de_name   = response.xpath(tb + '/tr[4]/td[3]/text()' ).extract_first().strip().replace(' ','').replace('\r\n','')
            de_flag   = response.xpath(tb + '/tr[5]/td[3]/text()' ).extract_first().strip().replace(' ','').replace('\r\n','')
            de_desc   = response.xpath(tb + '/tr[10]/td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            de_type   = response.xpath(tb + '/tr[14]/td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            de_format = response.xpath(tb + '/tr[15]/td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            de_allow  = response.xpath(tb + '/tr[16]/td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            if de_allow=="":
                de_allow='-'
            f.write(de_name + "|" 
                + de_flag + "|" 
                + de_desc + "|" 
                + de_type + "|"
                + de_format + "|" 
                + de_allow
                + "\n") 
        
        print "-----------parse_detail end-------------"