# -*- coding: utf-8 -*-
import scrapy
from hita.items import HitaItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "cv2"
    allowed_domains = ["omaha.org.cn"]
    stop_time = 0
    home_url = "http://meta.omaha.org.cn"

    def start_requests(self):
        urls = []

        #从word中获取需要查询的单词
        word_file = open('./urls_cv.txt', 'r')
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

        with open('CV/' + FileName + ".txt","a") as f:
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

        #/html/body/div[2]/div[1]/div[2]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[3]
        #print response.xpath('/html/body/div[2]/div[1]/div[2]/table/tr[3]/td/table/tr[2]/td[3]/text()').extract_first()

        xpath_left = '/html/body/div[2]/div[1]/div[2]/table/tr[3]/td/table/tr['
        xpath_right = ']/td[3]/text()'
        de_name   = response.xpath(xpath_left + '2'  + xpath_right).extract_first().strip().replace(' ','').replace('\r\n','')
        de_flag   = response.xpath(xpath_left + '3'  + xpath_right).extract_first().strip().replace(' ','').replace('\r\n','')
        de_defy   = response.xpath(xpath_left + '4' + xpath_right).extract_first()
        try:
            de_defy.strip().replace(' ','').replace('\r\n','')
        except:
            de_defy = ''
        de_desc   = response.xpath(xpath_left + '5' + xpath_right).extract_first()
        try:
            de_desc.strip().replace(' ','').replace('\r\n','')
        except:
            de_desc = ''

        print de_name
        #print de_flag
        #print de_defy
        #print de_desc
        line = ''
        
        #/html/body/div[2]/div[1]/div[2]/table/tbody/tr[5]/td/table
        for sel in response.xpath('/html/body/div[2]/div[1]/div[2]/table/tr[5]/td/table/tr'):
            de_val  = ''
            try:
                de_val = sel.xpath('td[2]/text()').extract_first()
            except:
                de_val  = ''

            de_val_desc = ''
            try:
                de_val_desc = sel.xpath('td[3]/text()').extract_first()
            except:
                de_val_desc = ''

            if de_val !='值':
                line += de_name + "|" \
                    + de_flag + "|" \
                    + de_defy + "|" \
                    + de_desc + "|" \
                    + de_val + "|" \
                    + de_val_desc \
                    + "\n"
#
        with open( 'CV/' + FileName + "_detail.txt","a") as f:
            f.write(line) 
        
        print "-----------parse_detail end-------------"