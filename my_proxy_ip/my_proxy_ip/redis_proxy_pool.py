import redis
from my_proxy_ip import settings

class CustomError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class RedisClient(object):
    def __init__(self, list_name=settings.LIST_NAME, host=settings.HOST, port=settings.PORT):
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




