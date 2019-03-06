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
        """
        请求重试中间件的处理
        """
        if request.meta.get('dont_retry', False):
            # 如果请求接口设置了不进行重试，就不进行重试直接返回
            return response
        if response.status in self.retry_http_codes:
            # 判断响应状态码是否在重试的状态码列表之中
            reason = response_status_message(response.status)
            print('响应状态吗在错误码中，更换当前IP {}'.format(request.meta['proxy'][8:]))
            try:
                # redis中删除当前代理
                request.meta['proxy'] = self.delete_proxy(
                    request.meta['proxy'][8:])
            except BaseException as e:
                self.logger.warning('请求代理存在异常 {}'.format(e))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        """
        重试异常处理
        """
        # 当重试的异常在异常列表中，进行删除代理的处理
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            print('发生异常更换当前IP {}'.format(request.meta['proxy'][8:]))
            try:
                request.meta['proxy'] = self.delete_proxy(
                    request.meta['proxy'][8:])
                time.sleep(random.randint(3, 5))
            except BaseException as e:
                self.logger.warning('请求代理存在异常 {}'.format(e))
            return self._retry(request, exception, spider)
