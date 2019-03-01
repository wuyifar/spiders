import redis
import requests
import json

pool = redis.ConnectionPool(
    host='localhost', port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)


class RandomProxy(object):
    def process_request(self, request, spider):
        if r.randomkey():
            proxy = r.randomkey()
            request.meta['proxy'] = 'https://{}'.format(proxy)
        else:
            response = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=773ad987cd9245f59eb722d74a23485f&orderno=YZ20193115018tWxk6&returnType=2&count=1')
            data = json.loads(response.text)
            results= data['RESULT']
            for result in results:
                print(result)
                port = result['port']
                ip = result['ip']
                proxy_str = ip + ':' + port
                r.set(proxy_str, 'True')
                request.meta['proxy'] = 'https://{}'.format(proxy_str)
