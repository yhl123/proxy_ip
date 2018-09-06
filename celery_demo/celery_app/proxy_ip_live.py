import redis
import requests
from celery_app import app

PORT = 6379
HOST = '127.0.0.1'
LIST_NAME = 'proxy_ip'


class CustomError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class RedisClient(object):
    def __init__(self, list_name=LIST_NAME, host=HOST, port=PORT):
        self.list_name = list_name  # 默认动态代理池name：proxy_ip
        pool = redis.ConnectionPool(host=host, port=port)
        self._db = redis.Redis(connection_pool=pool)

    def get(self, count=1):
        proxies = self._db.lrange(self.list_name, 0, count - 1)
        self._db.ltrim(self.list_name, count, -1)
        return proxies

    def put(self, proxy):
        self._db.rpush(self.list_name, proxy)

    def list_len(self):
        return self._db.llen(self.list_name)

    def look_list(self):
        return self._db.lrange(self.list_name, 0, -1)

    def pop(self):
        try:
            return self._db.rpop(self.list_name).decode('utf-8')
        except:
            raise CustomError('代理IP已用完')


@app.task
def get_proxy_ip_live():
    print(44)
    r = RedisClient()
    proxy_ip_content = (r.get()[-1]).decode('utf8')
    proxy_ip_type, proxy_ip = proxy_ip_content.split(':', maxsplit=1)
    try:
        s = requests.session()
        s.get(url='http://ip.seofangfa.com/checkproxy/', proxies={
            "%s" % (proxy_ip_type): "%s" % (proxy_ip)})
    except:
        return 'ip代理失败'
    else:
        r.put(proxy_ip_content)


@app.task
def get_proxy_ip_count():
    pass  # 执行你的scrapy项目
