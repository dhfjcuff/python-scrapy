
# user - agent中间件

from faker import Faker


class UserAgent_Middleware():

    def process_request(self, request, spider):
        f = Faker()
        agent = f.firefox()
        request.headers['User-Agent'] = agent


# 代理ip中间件

import requests
class Proxy_Middleware():

    def process_request(self, request, spider):

        try:
            xdaili_url = spider.settings.get('XDAILI_URL')

            r = requests.get(xdaili_url)
            proxy_ip_port = r.text
            request.meta['proxy'] = 'https://' + proxy_ip_port
        except requests.exceptions.RequestException:
            print('获取讯代理ip失败！')
            spider.logger.error('获取讯代理ip失败！')


# scrapy中对接selenium

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from gp.configs import *


class ChromeDownloaderMiddleware(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 设置无界面
        if CHROME_PATH:
            options.binary_location = CHROME_PATH
        if CHROME_DRIVER_PATH:
            self.driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)  # 初始化Chrome驱动
        else:
            self.driver = webdriver.Chrome(chrome_options=options)  # 初始化Chrome驱动

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        try:
            print('Chrome driver begin...')
            self.driver.get(request.url)  # 获取网页链接内容
            return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                status=200)  # 返回HTML数据
        except TimeoutException:
            return HtmlResponse(url=request.url, request=request, encoding='utf-8', status=500)
        finally:
            print('Chrome driver end...')


# scrapy对接cookie中间件
class WeiBoMiddleWare(object):
    def __init__(self, cookies_pool_url):
        self.logging = logging.getLogger("WeiBoMiddleWare")
        self.cookies_pool_url = cookies_pool_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_pool_url)
        except Exception as e:
            self.logging.info('Get Cookies failed: {}'.format(e))
        else:
            # 在中间件中，设置请求头携带的Cookies值，必须是一个字典，不能直接设置字符串。
            cookies = json.loads(response.text)
            self.logging.info('Get Cookies success: {}'.format(response.text))
            return cookies

    @classmethod
    def from_settings(cls, settings):
        obj = cls(
            cookies_pool_url=settings['WEIBO_COOKIES_URL']
        )
        return obj

    def process_request(self, request, spider):
        request.cookies = self.get_random_cookies()
        return None
