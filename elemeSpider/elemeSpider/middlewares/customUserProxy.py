import redis
import requests
import json

pool = redis.ConnectionPool(
    host='localhost', port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)


class RandomProxy(object):
    def process_request(self, request, spider):
        print('运行代理管理模块')
        if r.randomkey():
            proxy = r.randomkey()
            request.meta['proxy'] = 'https://{}'.format(proxy)
        else:
            print('代理池IP为空')
