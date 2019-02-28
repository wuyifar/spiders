import redis
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
import scrapy

class HttpErrorMiddleware(object):
    def process_response(self, request, response, spider):
        print('打印现在的状态码{}'.format(response.status))
        if response.status < 200 or response.status > 300:
            pool = redis.ConnectionPool(
                host='localhost', port=6379, decode_responses=True, db=0)
            r = redis.Redis(connection_pool=pool)
            r.flushdb()
            print('相应状态码不正常')
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
        return request
