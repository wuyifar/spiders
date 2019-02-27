from scrapy.contrib.downloadermiddleware.cookies import CookiesMiddleware
from elemeSpider.middlewares.resource import cookies 
import random


def make_cookie(cookie_str):
    cookies = {}
    cookie_list = cookie_str.split(';')
    for i in cookie_list:
        a, b = i.split('=')
        cookies[a] = b
    return cookies

class RandomCookie(CookiesMiddleware):
    def process_request(self, request, spider):
        cookie = make_cookie(random.choice(cookies))
        request.cookies = cookie