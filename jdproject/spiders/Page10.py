# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from urllib import parse
from scrapy_splash.request import SplashRequest, SplashFormRequest
from jdproject.items import JdprojectItem
import time
flg=1
class Demo1Spider(scrapy.Spider):
    name = "Page10"
    allowed_domains = ['baidu.com', 'cnblogs.com','blog.csdn.net']

    def __init__(self, category=None, *args, **kwargs):
        super(Demo1Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.baidu.com/s?ie=UTF-8&wd=POJ/%s' % category]

    #start_urls = ['https://www.baidu.com/s?ie=UTF-8&wd=poj4001', ]
    #for i in range(4002,4010):
      #  str = '%d' % i
        #start_urls.append('https://www.baidu.com/s?ie=UTF-8&wd=poj'+str)

    splash_arg = {"lua_source": """
                        --splash.response_body_enabled = true
                        splash.private_mode_enabled = false
                        splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                        splash:go(splash.args.url)  
                        splash:wait(10)
                        return {html = splash:html()}
                        """}
    def parse(self, response):
        global  flg
        print("进入parse")
        print(response.url)
        number = response.url[-4:]
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            #yield SplashRequest(url=li, endpoint='run', args=self.splash_arg, callback=self.detail_parse,meta={"number":number})

            m = 0
            while flg != 1:
                time.sleep(1)
                m += 1
                if m > 8:#原本20
                    print("超时了")
                    flg = 1
            flg = 0


            yield scrapy.Request(url=li, callback=self.detail_parse, meta={
                'splash': {
                    'args': {
                        # 在此处设置端点API的参数
                        'wait': 5,
                        'html': 1,

                    },
                    'render.html':{
                        'images':0,
                        'resource_timeout': 20,
                    },
                },
                "number" : number
            })


        '''
        list = response.xpath("//div[@id='page']//@href").extract()
        i = 2
        for li in list:
            hp = "https://www.baidu.com" + li
            print(hp)
            self.a=self.a+1
            print("a", end="")
            print(self.a)
            #yield scrapy.Request(url=hp, callback=self.parse_2, dont_filter=True,meta={"number":number})
            i = i + 1
            if i > 2:
                break
        '''
    def detail_parse(self, response):
        global flg
        if 'csdn.net' not in response.url and 'cnblogs.com' not in response.url:
            return
        if 'csdn.net' in response.url:
            m = JdprojectItem()
            content = response.xpath("//div[@class='blog-content-box']//text()").extract()
            s = " "
            for i in content:
                # s += i
                s += " ".join(i.split())
            h=s.replace("\xa0", "")
            m["url"]=response.url
            m["number"] = response.meta["number"]
            m["content"] = h
            yield m
            flg = 1
            return
        if 'cnblogs.com' in response.url:
            m = JdprojectItem()
            content = response.xpath("//div[@class='post']//text()").extract()
            s = " "
            for i in content:
                # s += i
                s += " ".join(i.split())
            h = s.replace("\xa0", "")
            m["url"] = response.url
            m["number"] = response.meta["number"]
            m["content"] = h
            yield m
            flg = 1
            return


    def parse_2(self, response):
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            self.b=self.b+1
            print("b", end="")
            print(self.b)
            yield SplashRequest(url=li, endpoint='run', args=self.splash_arg, callback=self.detail_parse,meta={"number":response.meta["number"]})