# -*- coding: utf-8 -*-
import scrapy


class MyProxyIpItem(scrapy.Item):
    proxy_ip = scrapy.Field()
    proxy_ip_port = scrapy.Field()
    proxy_ip_type = scrapy.Field()
