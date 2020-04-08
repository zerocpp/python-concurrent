import redis


def decode_redis(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    if isinstance(value, (list, tuple, set)):
        return type(value)(map(decode_redis, value))
    return value


def get_now_iso_0800():
    import pytz
    import datetime
    import time
    return datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).isoformat()


def log(msg):
    print(f'{get_now_iso_0800()} {msg}', flush=True)


def get_url_from_params():
    from zsysargs import get_all_params
    params = get_all_params()
    return params["REDIS_URL"]


def redis_connect(redis_url=None):
    if not redis_url:
        redis_url = get_url_from_params()
    return RedisClient(redis_url)


class RedisClient:
    def __init__(self, url):
        self.client = redis.from_url(url)

    def block_random_get(self, pattern, error_log='获取随机值失败，重试中....'):
        """阻塞随机获取值"""
        import time
        import random
        error_log_flag = False
        while True:
            try:
                keys = self.keys(pattern)
                if keys:
                    key = random.choice(keys)
                    value = self.get(key)
                    if value:
                        return value
            except:
                pass

            if not error_log_flag:
                error_log_flag = True
                log(error_log)

            time.sleep(1)

    def block_pop(self, key, wait_log='等待填充中'):
        if self.llen(key) <= 0:
            if wait_log:
                log(wait_log)
        return self.blpop(key)

    def block(self, key, wait_log='暂停'):
        """阻塞等待信号"""
        import time

        value = self.get(key)
        error_log_flag = False
        while value == 'block':
            if not error_log_flag:
                error_log_flag = True
                log(wait_log)
            time.sleep(1)
            value = self.get(key)

    def get(self, name):
        return decode_redis(self.client.get(name))

    def set(self, name, value):
        return self.client.set(name, value)

    def expire(self, name, ttl):
        return self.client.expire(name, ttl)

    def set_expire(self, name, value, ttl):
        self.set(name, value)
        return self.expire(name, ttl)

    def rename(self, src, dst):
        self.client.rename(src, dst)

    def sadd(self, name, value):
        return self.client.sadd(name, value)

    def sismember(self, name, value):
        return self.client.sismember(name, value)

    def keys(self, pattern='*'):
        return list(map(decode_redis, self.client.keys(pattern)))

    def sall(self, name):
        return list(map(decode_redis, self.client.sunion(name)))

    def sall_it(self, name):
        return (decode_redis(it) for it in self.client.sunion(name))

    def set2list(self, set_name, list_name):
        """convert set to list"""
        self.delete(list_name)
        return self.lpush(list_name, *self.sall(set_name))

    def sdiff(self, name, *value):
        return self.client.sdiff(name, *value)

    def delete(self, *names):
        return self.client.delete(*names)

    def lpush(self, name, *values):
        return self.client.lpush(name, *values)

    def llen(self, name):
        return self.client.llen(name)

    def blpop(self, keys, timeout=0):
        return decode_redis(self.client.blpop(keys, timeout))[-1]

    def lpop(self, name):
        return decode_redis(self.client.lpop(name))

    def rpop(self, name):
        return decode_redis(self.client.rpop(name))

    def brpop(self, keys, timeout=0):
        return decode_redis(self.client.brpop(keys, timeout))[-1]

    def lall(self, name):
        return [decode_redis(it) for it in self.client.lrange(name, 0, -1)]

    def lrem(self, name, value):
        self.client.lrem(name, 0, value)

    def lpopall(self, name):
        items = [decode_redis(it) for it in self.client.lrange(name, 0, -1)]
        self.client.delete(name)
        return items

    def rpush(self, name, *values):
        return self.client.rpush(name, *values)

    def rextends(self, name, key):
        """rpush the set"""
        values = self.sall(key)
        if values:
            return self.rpush(name, *values)
        else:
            return 0

    def list(self, name, *values):
        self.delete(name)
        return self.lpush(name, *values)


def main():
    redis_client = RedisClient()
    redis_client.lpush('x', 'x1')
    print(redis_client.keys())


if __name__ == '__main__':
    main()
