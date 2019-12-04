import scrapy
from scrapy_splash import SplashRequest
import time
import sys
import os
splash_arg = {"lua_source": """
                        --splash.response_body_enabled = true
                        splash.private_mode_enabled = false
                        splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                        splash:go(splash.args.url)  
                        splash:wait(20)
                        url = splash:url()
                        return {html = splash:html(),url
                        }
                        """}
flg = 1
class DemoSpider(scrapy.Spider):
    name = 'demo'
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
            while flg != 1:
                time.sleep(1)
                m += 1
                if m > 30:
                    flg = 1
            flg = 0
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
        global flg
        if 'csdn.net' not in response.url and 'cnblogs.com' not in response.url:
            return
        if 'csdn.net' in response.url:
            content = response.xpath("//div[@class='blog-content-box']//text()").extract()
            s = " "
            for i in content:
                # s += i
                s += " ".join(i.split())
            print("content:", end="")
            print(s.replace("\xa0", ""))
            print("url:", end="")
            print(response.url)
            return
        if 'cnblogs.com' in response.url:
            content = response.xpath("//div[@class='post']//text()").extract()
            s = " "
            for i in content:
                # s += i
                s += " ".join(i.split())
            print("content:", end="")
            print(s.replace("\xa0", ""))
            print("url:", end="")
            print(response.url)
            return
        content = response.xpath("//p//text()").extract()
        s = " "
        for i in content:
            #s += i
            s += "".join(i.split())
        print("content:", end="")
        print(s.replace("\xa0", ""))
        print("url:", end="")
        print(response.url)
        flg = 1
