# -*- coding: utf-8 -*-
import scrapy
import re
import time
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class SFLSGZHSpider(scrapy.Spider):
    name = "sflsgzh"
    
    def start_requests(self):
        start_urls = [
            'http://weixin.sogou.com/weixin?type=1&query=上外附中&ie=utf8',
            'http://weixin.sogou.com/weixin?type=1&query=sfls&ie=utf8'
        ]

        for url in start_urls:
            yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        for li in response.xpath('//ul[@class="news-list2"]/li'):
            url = li.xpath('div/div[1]/a/@href')
            img = li.xpath('div/div[1]/a/img/@src')
            name = striphtml(li.xpath('div/div[2]/p[1]/a').extract_first())
            info = li.xpath('div/div[2]/p[2]/label/text()').extract_first()
            data = li.xpath('div/div[2]/p[2]/text()').extract()
            try:
                data = re.split(u'月发文|篇|平均阅读',data[2])
                post_month = int(data[1])
                read_avg = int(data[3])
            except IndexError:
                post_month = 0
                read_avg = 0
           
            qrcode = li.xpath('div/div[3]/span/img[1]/@src')
            jieshao = striphtml(li.xpath('dl[1]/dd').extract_first())
            latest = li.xpath('dl[2]/dd/span/text()').extract_first()
            yield {
                'name': name,
                'info': info,
                'post_month': post_month,
                'read_avg': read_avg,
                'jieshao': jieshao,
                'latest': latest,
                'date': time.strftime("%Y-%m-%d",time.localtime())    
            }
        # continue for next page
        next_page = response.xpath('//a[@id="sogou_next"]/@href').extract_first()
        print next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)
