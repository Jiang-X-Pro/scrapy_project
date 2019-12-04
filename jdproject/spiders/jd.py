# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from urllib import parse
from scrapy_splash.request import SplashRequest, SplashFormRequest
from jdproject.items import JdprojectItem
import time
class JdSpider(scrapy.Spider):
    name = "jd"
    arg_1="""
                    --splash.response_body_enabled = true
                    splash.private_mode_enabled = false
                    splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
                    assert(splash:go(" """
    arg_2= """ "))
                    splash:wait(3)
                    return {html = splash:html()}
                    """
    allowed_domains = ['baidu.com', 'cnblogs.com','blog.csdn.net']
    start_urls = [
        'https://www.baidu.com/s?ie=UTF-8&wd=poj4001',
        ]
    for i in range(4002,4030):
        str = '%d' % i
        start_urls.append('https://www.baidu.com/s?ie=UTF-8&wd=poj'+str)

    splash_arg = {"lua_source": """
                        --splash.response_body_enabled = true
                        splash.private_mode_enabled = false
                        splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                        splash:go(splash.args.url)  
                        splash:wait(10)
                        return {html = splash:html()}
                        """}
    '''
    def start_request(self):
        splash_arg = {"lua_source": """
                    --splash.response_body_enabled = true
                    splash.private_mode_enabled = false
                    splash:set_user_agent(" Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                    assert(splash:go("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=poj4001&oq=quotes&rsv_pq=8a9cccb4000093a1&rsv_t=099fyXsRDU6sHZBjtrsC4og8KJw4hHtGc7HQSWIGxkyb3woJDJJrC4kKuFM&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=35857&rsv_sug3=29&rsv_sug1=32&rsv_sug7=101&rsv_sug2=0&rsv_sug4=36445&rsv_sug=1"))
                    splash:wait(3)
                    splash.images_enabled = True
                    return {html = splash:html()}
                    """}
        print(splash_arg)
        yield scrapy.Request(url="https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=poj4001&oq=poj4001&rsv_pq=d38edeca0003eae2&rsv_t=ac85Vyc9mYNJhviUZ9eq5uHgqFo61N%2Fr%2F%2BCyl8LdZ1UcGJ%2F1z2zhMoav1o0&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug=1", callback=self.onSave, dont_filter=True)
        '''
    def parse(self, response):
        print("进入parse")
        print(response.url)
        number = response.url[-4:]
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            print(li)
            #splash_args = {"lua_source":self.arg_1+li+self.arg_2}
            #print(splash_args)
            time.sleep(2)
            yield SplashRequest(url=li, endpoint='run', args=self.splash_arg, callback=self.detail_parse,meta={"number":number}, resource_timeout=20)
        list = response.xpath("//div[@id='page']//@href").extract()
        i = 2
        for li in list:
            hp = "https://www.baidu.com" + li
            print(hp)
            yield scrapy.Request(url=hp, callback=self.parse_2, dont_filter=True,meta={"number":number})
            i = i + 1
            if i > 2:
                break

    def detail_parse(self, response):
        m = JdprojectItem()
        print("进入detail_parse")
        print(response.meta["number"])
        print(response.url)
        content = response.xpath("//p//text()").extract()
        s = " "
        for i in content:
            s+=i
        h = s.replace("\xa0", "")
        print(h)
        m["url"] = response.meta["number"]
        m["content"] = h
        yield m

    def parse_2(self, response):
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            print(li)
            splash_args = {"lua_source": self.arg_1 + li + self.arg_2}
            print("yield")
            time.sleep(2)
            yield SplashRequest(url=li, endpoint='run', args=self.splash_arg, callback=self.detail_parse,meta={"number":response.meta["number"]},  resource_timeout=20)
