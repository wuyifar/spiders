from scrapy.contrib.downloadermiddleware.cookies import CookiesMiddleware
import random
import redis


def make_cookie(cookie_str):
    """
    Cookie字符串的处理
    """
    cookies = {}
    cookie_list = cookie_str.split('; ')
    for i in cookie_list:
        a, b = i.split('=')
        cookies[a] = b
    return cookies


class RandomCookie(CookiesMiddleware):
    """
    接口请求前修改cookie
    """
    def process_request(self, request, spider):
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True, db=2)
        r = redis.Redis(connection_pool=pool)
        cookie = make_cookie(r.get(r.randomkey()))
        request.cookies = cookie
