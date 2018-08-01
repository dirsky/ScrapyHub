# -*- coding: utf-8 -*-
import scrapy
from hita.items import HitaItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

class HitaSpider(scrapy.Spider):
    name = "ds2"
    allowed_domains = ["omaha.org.cn"]
    stop_time = 0
    home_url = "http://meta.omaha.org.cn"

    def start_requests(self):
        urls = []

        #从word中获取需要查询的单词
        word_file = open('./DS/Urls.txt', 'r')
        for one in word_file:
            one = one.replace('\r','').replace('\n','')
            #print one
            urls.append(one)            
        word_file.close()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)


    def parse_detail(self, response):
        print response.xpath('//title/text()').extract_first()
        print response.url
        print "-------------parse_detail---------------"

        #/html/body/div[2]/div[1]/div[2]/table
        xpath_left = '/html/body/div[2]/div[1]/div[2]/table'
        
        de_name   = response.xpath(xpath_left + '/tr[3]/td/table/tr[2]/td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
        de_flag   = response.xpath(xpath_left + '/tr[3]/td/table/tr[3]/td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
        
        de_Keyword   = response.xpath(xpath_left + '/tr[3]/td/table/tr[5]/td[3]/text()').extract_first()
        try:
            de_Keyword.strip().replace(' ','').replace('\r\n','')
        except:
            de_Keyword = '-'
        
        #/html/body/div[2]/div[1]/div[2]/table/tbody/tr[5]/td/table/tbody/tr[1]/td[3]
        de_desc = response.xpath(xpath_left + '/tr[5]/td/table/tr[1]/td[3]/text()').extract_first()
        try:
            de_desc.strip().replace(' ','').replace('\r\n','')
        except:
            de_desc = '-'

        #/html/body/div[2]/div[1]/div[2]/table/tr[13]/td/table/tr[1]/td[3]
        de_ver = response.xpath(xpath_left + '/tr[13]/td/table/tr[1]/td[3]/text()').extract_first()
        try:
            de_ver.strip().replace(' ','').replace('\r\n','')
        except:
            de_ver = '-'

        print de_name
        print de_flag
        print de_desc
        print de_Keyword
        #print de_ver

        line = ''       
        line += de_name + "\n" \
            + de_flag + "\n" \
            + de_desc + "\n" \
            + de_Keyword + "\n" \
            + de_ver + "\n" \
            + "\n"

        with open( 'DS/' + de_flag + "_Head.txt","a") as f:
            f.write(line) 
        
        #调用详情页面

        #http://meta.omaha.org.cn/elementOfSetList/get?subset=&dataSetCode=HDSB01.01
        url = 'http://meta.omaha.org.cn/elementOfSetList/get?subset=&dataSetCode='
        url += de_flag
        yield scrapy.Request(url=url, callback=self.parse_page)

        print "-----------parse_detail end-------------"


    def parse_page(self, response):
        print response.xpath('//title/text()').extract_first()
        print "------------parse_page start------------"

        pageNo = response.css('ul.page li')[-2].css('a::text').extract_first()
        print "共有" + pageNo + "页"
        #http://meta.omaha.org.cn/elementOfSetList/get?subset=&dataSetCode=HDSA00.01
        #http://meta.omaha.org.cn/elementOfSetList/get?subset=&dataSetCode=HDSB01.01&pageNo=1

        for i in range(1, int(pageNo)+1):
            url = response.url + "&pageNo=" + str(i)
            print url
            yield scrapy.Request(url=url,callback=self.parse_value)

        print "----------------end--------------------"

    
    def parse_value(self, response):
        print response.xpath('//title/text()').extract_first()
        print response.url
        print "-------------parse_value---------------"

        #/html/body/div[2]/div[1]/div[2]/table/tr[1]/td[1]
        #print response.xpath('/html/body/div[2]/div[1]/div[2]/table').extract_first()

        line = ''
        ref = ''
        for li in response.xpath('/html/body/div[2]/div[1]/div[2]/table/tbody/tr'):
            #print li.extract()
            inflag = ''
            try:
                inflag     = li.xpath('td[1]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            except:
                inflag = '-'
            
            name = ''
            try:
                name       = li.xpath('td[2]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            except:
                name = '-'
            outflag    = li.xpath('td[3]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            
            defy = ''
            try:
                defy       = li.xpath('td[4]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            except:
                defy = '-'
            
            dataType = ''
            try:
                dataType   = li.xpath('td[5]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            except:
                dataType = '-'
            
            dataFormat = ''
            try:
                dataFormat = li.xpath('td[6]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
            except:
                dataFormat = '-'
            
            valueAllow = ''
            try:
                valueAllow = li.xpath('td[7]/text()').extract_first().strip().replace(' ','').replace('\r\n','')
                if valueAllow != '-':
                    try:
                        valueAllow = li.xpath('td[7]/a/text()').extract_first().strip().replace(' ','').replace('\r\n','')
                    except:
                        print 'valueAllow'
            except:
                valueAllow = '-'
            if valueAllow != '-':
                ref += valueAllow + "\n"
                
            print inflag + name
            #print li.xpath('td[7]/a/text()').extract_first()
       
            line += inflag + "|" \
                + name + "|" \
                + outflag + "|" \
                + defy + "|" \
                + dataType + "|" \
                + dataFormat + "|" \
                + valueAllow + "\n" 
        filename = response.url.split('=')[2][:9]
        with open( 'DS/' + filename + "_Body.txt","a") as f:
            f.write(line) 
        with open( 'DS/' + filename + "_Ref.txt","a") as f:
            f.write(ref) 
        
        ##调用详情页面
        
        print "-----------parse_value end-------------"