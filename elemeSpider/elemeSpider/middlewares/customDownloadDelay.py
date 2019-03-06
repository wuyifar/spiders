from elemeSpider.middlewares.resource import RAMDOM_TIME
import random
import time


class RandomDelay(object):
    """
    设置每个请求的时间间隔
    """
    def process_request(self, request, spider):
        sleep_time = random.choice(RAMDOM_TIME)
        print('访问间隔时间{}'.format(sleep_time))
        time.sleep(sleep_time)
