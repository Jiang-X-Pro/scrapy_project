# -*- coding: utf-8 -*-
import scrapy
from jdproject.items import JdprojectItem
from urllib import parse
class BaiduSpiderSpider(scrapy.Spider):
    name = 'baidu_spider'
    allowed_domains = ['baidu.com', 'cnblogs.com']
    start_urls = ['https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=poj4001&rsv_pq=96ffe63500051213&rsv_t=eadbaANVToFtS%2Ft7akKf0xcJYFKLIF4I9wiCVxIvS6v2KcNV26w%2BTQU2Ixw&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=9&rsv_sug1=4&rsv_sug7=100&rsv_sug2=0&inputT=11003&rsv_sug4=13684',]

    def parse(self, response):
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            print(li)
            yield scrapy.Request(url=li, callback=self.detail_parse,dont_filter=True)
        list = response.xpath("//div[@id='page']//@href").extract()
        i = 2
        for li in list:
            hp="https://www.baidu.com"+li
            print(hp)
            yield scrapy.Request(url=hp, callback=self.parse_2, dont_filter=True)
            i = i + 1
            if i > 5:
                break
    def detail_parse(self, response):
        #print(response.callback)
        if "cnblogs.com" in response.url :
            print(response.url)
            content = response.xpath("//p//text()").extract()
            s=" "
            for i in content:
                s+=i
            print(s.replace("\xa0", ""))
    def parse_2(self, response):
        page_list = response.xpath("//div[@id='content_left']//h3//@href").extract()
        for li in page_list:
            print(li)
            yield scrapy.Request(url=li, callback=self.detail_parse, dont_filter=True)

