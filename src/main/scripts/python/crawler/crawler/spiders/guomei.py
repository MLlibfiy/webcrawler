# encoding=utf-8

import urllib
import js2xml
from bs4 import BeautifulSoup
from lxml import etree
import scrapy
import re
import json
import time
import random


# 自定义类
class ItemList(scrapy.Spider):
    # 爬虫的名字
    name = 'guomei'

    keyword = "手机"

    # 防止请求被拦截
    headers = {
        ":authority": "search.gome.com.cn",
        ":method": "GET",
        ":path": "/search?search_mode=normal&reWrite=true&question=%E6%89%8B%E6%9C%BA&searchType=goods&&page=3&type=json&aCnt=0&reWrite=true",
        ":scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&searchType=goods&search_mode=normal&reWrite=true",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    # base_url = "https://search-x.jd.com/Search?callback=jQuery7201478&area=1&enc=utf-8&keyword=%s" \
    #            "&adType=7&urlcid3=655&page=%d&ad_ids=291%%3A33&xtest=new_search&_=1549863368204"

    base_url = "https://search.gome.com.cn/search?search_mode=normal&reWrite=true&question=%E6%89%8B%E6%9C%BA&searchType=goods&&page=2&type=json&aCnt=0&reWrite=true"

    # base_url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4158&productId=18180353715&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1"

    # 存放结果的集合
    result_list = []

    # 发起请求的方法，第一个被调用的
    def start_requests(self):
        for page in range(1, 3, 2):
            self.headers[':path'] = self.base_url
            # url 请求地址
            # callback 回调函数
            # headers 请求头
            yield scrapy.Request(url=self.base_url, callback=self.parse, headers=self.headers)

    # 回调函数，请求成功之后调用
    def parse(self, response):
        content = json.loads(response.text)
        products = content['content']['prodInfo']['products']
        for product in products:
            promoDesc = product['promoDesc']
            name = product['name']
            pId = product['pId']

            #print("%s\t%s\t%s" % (pId, name, promoDesc))

            url = "https://item.gome.com.cn/%s.html" % pId
            print(url)
            time.sleep(random.randint(1, 3))
            yield scrapy.Request(url=url, callback=self.parse2, headers=self.headers)

    def parse2(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        src = soup.select("html head script")[1].string
        src_text = js2xml.parse(src, debug=False)
        src_tree = js2xml.pretty_print(src_text)
        print(src_tree)
        selector = etree.HTML(src_tree)
        for i in selector.xpath("//property[@name = 'ColorVersion']/object"):
            print(i.xpath("./property/string/text()"))
            print(i.xpath("./property/@name"))



    # 最后调用的方法
    def closed(self, reason):
        print("结束")
