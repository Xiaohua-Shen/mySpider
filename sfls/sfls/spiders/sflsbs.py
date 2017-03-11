import scrapy

class SFLSBSSpider(scrapy.Spider):
    name = "sflsbs"

    def start_requests(self):
        url = 'http://gaokao.chsi.com.cn/zsgs/bssnlqmd--method-groupByYx,year-2008.dhtml'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for school in response.xpath('//div[@id="cnt1"]/ul/li/a'):
            next_page = school.css('a::attr(href)').extract_first()
            print next_page
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, self.parse_school) 
    
    def parse_school(self, response):
        school_name = response.xpath('//h2/text()')[1].re(r'\((.*)\)')
        for student in response.xpath('//table[@id="YKTabCon2_10"]/tr[not(@class="bg_color02")]'):
            yield {
                'school': school_name,
                'name': student.css('td')[0].re(r'<td.*>(.*)</td>'),
                'sex': student.css('td')[1].re(r'<td.*>(.*)</td>'),
                'province': student.css('td')[2].re(r'<td.*>(.*)</td>'),
                'from_school': student.css('td')[3].re(r'<td.*>(.*)</td>'),
                'reason': student.css('td::text')[4].extract().strip(), 
                'score': student.css('td')[5].re(r'<td.*>(.*)</td>'),
                'score_line': student.css('td')[6].re(r'<td.*>(.*)</td>'),
                'major': student.css('td')[7].re(r'<td.*>(.*)</td>')
            }

