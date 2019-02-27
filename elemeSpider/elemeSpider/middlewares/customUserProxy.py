import redis

pool = redis.ConnectionPool(
    host='localhost', port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)


class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = r.randomkey()
        request.meta['proxy'] = 'https://{}'.format(proxy)
