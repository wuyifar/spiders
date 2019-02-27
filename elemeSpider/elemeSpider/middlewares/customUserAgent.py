from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from elemeSpider.middlewares.resource import USER_AGENT_LIST
import random


class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENT_LIST)
        request.headers.setdefault('User-Agent', useragent)