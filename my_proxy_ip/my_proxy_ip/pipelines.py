# -*- coding: utf-8 -*-
import requests
from my_proxy_ip import redis_proxy_pool


class MyProxyIpPipeline(object):
    def __init__(self):
        self.redis_client = redis_proxy_pool.RedisClient()
        self.s = requests.session()
        self.get_ip_live_url = 'http://ip.seofangfa.com/checkproxy/'

    def open_spider(self, spider):
        print('正在进行智能持久化')

    def process_item(self, item, spider):
        try:
            res = self.s.get(url=self.get_ip_live_url, proxies={
                "%s" % item['proxy_ip_type']: "%s:%s" % (item['proxy_ip'], item['proxy_ip_port'])})
        except:
            return 'ip代理失败'
        else:
            proxy_ip = ("%s:%s:%s" % (item['proxy_ip_type'], item['proxy_ip'], item['proxy_ip_port'])).encode('utf8')
            if self.redis_client.list_len() >= 200:
                return item
            else:
                self.redis_client.put("%s:%s:%s" % (item['proxy_ip_type'], item['proxy_ip'], item['proxy_ip_port']))
        return item

    def close_spider(self, spider):
        print('持久化已经完成', self.redis_client.look_list())
