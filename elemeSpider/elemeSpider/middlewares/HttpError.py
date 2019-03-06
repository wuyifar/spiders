import redis
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
import scrapy
import requests
import json


class HttpErrorMiddleware(object):
    def process_response(self, request, response, spider):
        print('打印现在的状态码{}'.format(response.status))
        print(request.cookies)
        if response.status < 200 or response.status > 300:
            pool = redis.ConnectionPool(
                host='localhost', port=6379, decode_responses=True, db=0)
            r = redis.Redis(connection_pool=pool)
            proxy_str = request.meta['proxy'][8:]
            try:
                r.delete(proxy_str)
            except BaseException as e:
                print('当前的IP已经不存在')
            print('相应状态码不正常')
        set_cookies = response.headers.getlist('Set-Cookie')
        try:
            set_cookies_str = set_cookies[0].decode()
        except BaseException as e:
            print('当前接口没有设置cookie')
            return response
        set_cookie_list = set_cookies_str.split('; ')
        a, b = set_cookie_list[0].split('=')
        USERID = request.cookies['USERID']
        request.cookies[a] = b
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True, db=2)
        r = redis.Redis(connection_pool=pool)
        cookie_str = ""
        print(request.cookies)
        for key, value in request.cookies.items():
            cookie_str = cookie_str + key + '=' + value
            cookie_str = cookie_str + '; '
        cookie_str = cookie_str[:-2]
        r.set(USERID, cookie_str)
        return response

    def process_exception(self, request, exception, spider):
        ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                          ConnectionRefusedError, ConnectionDone, ConnectError,
                          ConnectionLost, TCPTimedOutError, ResponseFailed,
                          IOError, TunnelError)
        if isinstance(exception, ALL_EXCEPTIONS):
            print('当前的异常是{}'.format(exception))
            pool = redis.ConnectionPool(
                host='localhost', port=6379, decode_responses=True, db=0)
            r = redis.Redis(connection_pool=pool)
            proxy_str = request.meta['proxy'][8:]
            print(proxy_str)
            r.delete(proxy_str)
            proxy_str = r.randomkey()
            request.meta['proxy'] = 'https://{}'.format(proxy_str)
        return request
