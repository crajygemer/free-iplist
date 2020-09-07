import scrapy
from scrapy.http import Request

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['us-proxy.org']
    start_urls = ['http://us-proxy.org/']

    def parse(self, response):
        table = response.xpath('//*[contains(@class, "table-striped")]')
        trs = table.xpath('.//tr')
        for tr in trs:
            ips = tr.xpath('.//td[1]/text()').extract_first()
            port = tr.xpath('.//td[2]/text()').extract_first()
            country_code = tr.xpath('.//td[3]/text()').extract_first()
            country = tr.xpath('.//td[4]/text()').extract_first()

            yield {
                "IP": ips,
                "Port": port,
                "Code": country_code,
                "Country": country
            }

        next_page = response.xpath('//*[@id="proxylisttable_next"]/a/@href').extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield Request(next_page)


