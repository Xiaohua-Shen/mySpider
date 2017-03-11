import scrapy
import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class SFLSGZHSpider(scrapy.Spider):
    name = "sflsgzh"

    def start_requests(self):
        url = 'http://weixin.sogou.com/weixin?type=1&query=sfls&ie=utf8'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for li in response.xpath('//ul[@class="news-list2"]/li'):
            url = li.xpath('div/div[1]/a/@href')
            img = li.xpath('div/div[1]/a/img/@src')
            name = striphtml(li.xpath('div/div[2]/p[1]/a').extract_first())
            info = li.xpath('div/div[2]/p[2]/label/text()').extract_first()
            qrcode = li.xpath('div/div[3]/span/img[1]/@src')
            jieshao = striphtml(li.xpath('dl[1]/dd').extract_first())
            renzhen = li.xpath('dl[2]/dd/text()').extract_first()
            yield {
                'name': name,
                'info': info,
                'jieshao': jieshao    
            }
'''
        # continue for next page
        next_page = response.xpath('//a[@id="sogou_next"]/@href').extract_first()
        print next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)
'''

