# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from my_proxy_ip.items import MyProxyIpItem


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['www.kuaidaili.com/free']
    start_urls = ['http://www.kuaidaili.com/free/']

    def parse(self, response):
        url_header = 'https://www.kuaidaili.com'
        tage_hrefs = response.xpath('//*[@id="listnav"]/ul/li/a/@href').extract()
        contents = response.xpath('//*[@id="list"]/table/tbody/tr')
        for content in contents:
            proxy_ip = content.xpath('./td[1]/text()').extract()[-1]
            proxy_ip_port = content.xpath('./td[2]/text()').extract()[-1]
            proxy_ip_type = content.xpath('./td[4]/text()').extract()[-1]
            yield MyProxyIpItem(proxy_ip=proxy_ip, proxy_ip_port=proxy_ip_port, proxy_ip_type=proxy_ip_type)

        # 遍历所有页
        for tage_href in tage_hrefs:
            yield Request(url=url_header + tage_href, callback=self.parse)
