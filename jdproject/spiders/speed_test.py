import scrapy
from scrapy_splash import SplashRequest
import time
import sys
import os
class Speed_testSpider(scrapy.Spider):
    name = 'speed_test'
    allowed_domains = ['jd.com', 'baidu.com', 'csdn.net']
    start_urls = [
                  "https://www.baidu.com/s?ie=UTF-8&wd=POJ4001"]

    def parse(self, response):
        global flg
        print("进入parse")
        print(response.url)
        number = response.url[-4:]
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            print(li)
            # splash_args = {"lua_source":self.arg_1+li+self.arg_2}
            # print(splash_args)
            #yield SplashRequest(url=li, endpoint='run', args=splash_arg, callback=self.parse1, meta={"number": number})
            m = 0
            yield scrapy.Request(url=li, callback=self.parse1 , meta={
                'splash': {
                    'args': {
                        # 在此处设置端点API的参数
                        'wait':15,
                        'html': 1,
                    },
                    'render.html':{
                        'images':0,
                        'resource_timeout':20,
                    },
                }
            })

    #def start_requests(self):
     #   for url in self.start_url:
     #       time.sleep(1)parse1
     #       yield SplashRequest(url=url, endpoint='run', args=splash_arg, callback=self.parse1,meta={"number":"1"})

    def parse1(self, response):
        print(response.url)
        print(response.text)
