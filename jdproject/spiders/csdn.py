# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy_splash.request import SplashRequest, SplashFormRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class CsdnSpider(scrapy.Spider):
    name = "csdn"
    allowed_domains = ['baidu.com', 'cnblogs.com']

    def start_requests(self):
        splash_args = {"lua_source": """
                    --splash.response_body_enabled = true
                    splash.private_mode_enabled = false
                    splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                    splash:go(splash.args.url)  
                    splash:wait(3)
                    splash.args.url = splash:url()
                    return {html = splash:html()}
                    """}
        url1 = "http://www.baidu.com/link?url=AJ8OQHrym-f-c3s_rvD4rQ_MXdmqOVinKQs7OVvIgNUbfuiRe0MIx-HZrRwlG61kd2jEiDlxaEOt-SJiB2YuK8dnqvsyGgLuuvS2OB9Hkpa"
        yield SplashRequest(url1, endpoint='run', args=splash_args, callback=self.onSave)

    def onSave(self, response):
        print(response.url)
        print(response.text)
    def detail_parse(self,response):
        print(response.url)
        print("saadsd")
        urls = {"111":response.url}
        yield urls