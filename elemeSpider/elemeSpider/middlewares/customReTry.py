from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import logging
import time
import random
import redis

pool = redis.ConnectionPool(
    host='localhost', port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)


class DiyRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def delete_proxy(self, proxy):
        """
        删除当前不可用的的代理，并返回新的代理
        """
        try:
            r.delete(proxy)
        except BaseException as e:
            print('当前代理不存在')
        new_proxy = r.randomkey()
        return 'https://{}'.format(new_proxy)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            print('重试更换当前IP')
            try:
                request.meta['proxy'] = self.delete_proxy(
                    request.meta['proxy'][8:])
                time.sleep(random.randint(3, 5))
            except BaseException as e:
                self.logger.warning('请求代理存在异常 {}'.format(e))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            print('重试更换当前IP')
            try:
                request.meta['proxy'] = self.delete_proxy(
                    request.meta['proxy'][8:])
                time.sleep(random.randint(3, 5))
            except BaseException as e:
                self.logger.warning('请求代理存在异常 {}'.format(e))
            return self._retry(request, exception, spider)
