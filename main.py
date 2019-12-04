from scrapy import  cmdline
import time
import sys
import os
'''
a='scrapy crawl Page10 -a category='
b=sys.argv[1]
c=a+str(b)
cmdline.execute(c.split())
'''
for i in range(4011,4021):
    a='scrapy crawl Page10 -a category='
    b=i
    c=a+str(b)
    os.system(c)