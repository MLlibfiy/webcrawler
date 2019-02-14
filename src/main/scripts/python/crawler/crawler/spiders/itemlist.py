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
    name = 'itemlist'

    keyword = "手机"

    # 防止请求被拦截
    headers = {
        ":authority": "sclub.jd.com",
        ":method": "GET",
        ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language:": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "cookie": "t=8444fb486c0aa650928d929717a48022; _tb_token_=e66e31035631e; cookie2=104997325c258947c404278febd993f7",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    # base_url = "https://search-x.jd.com/Search?callback=jQuery7201478&area=1&enc=utf-8&keyword=%s" \
    #            "&adType=7&urlcid3=655&page=%d&ad_ids=291%%3A33&xtest=new_search&_=1549863368204"

    base_url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&page=%d"

    # base_url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4158&productId=18180353715&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1"

    # 存放结果的集合
    result_list = []

    # 发起请求的方法，第一个被调用的
    def start_requests(self):

        for page in range(1, 3, 2):
            url = self.base_url % (urllib.quote(self.keyword), urllib.quote(self.keyword), page)
            print(url)

            self.headers[':path'] = self.base_url
            # url 请求地址
            # callback 回调函数
            # headers 请求头
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    # 回调函数，请求成功之后调用
    def parse(self, response):
        # content = json.loads(response.text[response.text.find('(')+1:-2])
        # response.text 获取响应体
        # 转换成json
        #for each in response.xpath("//li[@class='gl-item']"):
        id = response.xpath("//li[@class='gl-item']")[0].xpath("@data-sku").extract()[0]

        new_url = "https://item.jd.com/%s.html" % id

        print(new_url)
        #time.sleep(random.randint(1, 3))
        yield scrapy.Request(url=new_url, callback=self.parse2, headers=self.headers)

    def parse2(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        src = soup.select("html head script")[0].string
        src_text = js2xml.parse(src, debug=False)
        src_tree = js2xml.pretty_print(src_text)
        selector = etree.HTML(src_tree)

        for l in selector.xpath("//property[@name = 'colorSize']/array/object"):
            id = l.xpath("./property/number/@value")
            color = l.xpath("./property/string/text()")
            print(id)
            print(",".join(color))

            url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv55169&productId=%s&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1"
            new_url = url % id[0]
            time.sleep(random.randint(1, 3))
            yield scrapy.Request(url=new_url, callback=self.parse3, headers=self.headers)

    def parse3(self, response):
        print(response.text)
        p = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
        r = re.findall(p, response.text)
        content = json.loads(r[0])
        # # 获取评价列表
        comments = content['comments']

        for comment in comments:
            # 空字典
            item = {}
            item['content'] = comment['content']  # 评论正文
            item['guid'] = comment['guid']  # 用户id
            item['id'] = comment['id']  # 评论id
            item['time'] = comment['referenceTime']  # 评论时间
            item['color'] = self.parse_kuohao(comment['productColor'])  # 商品颜色
            item['size'] = self.parse_kuohao(comment['productSize'])  # 商品尺码
            item['userClientShow'] = comment['userClientShow']  # 购物渠道

            print(comment['content'])
            print(comment['guid'])
            print(comment['id'])
            print(comment['productColor'])
            print(comment['productSize'])
            print(comment['userClientShow'])
            print(comment['score'])
            print(comment['nickname'])
            print(comment['referenceId'])
            print(comment['referenceTime'])
            print(comment['referenceName'])

            print("="*100)

    # 最后调用的方法
    def closed(self, reason):
        print("结束")

    # 干掉括号
    def parse_kuohao(self, text):
        new_text = text
        searchObj1 = re.search(r'（.+）', text, re.M | re.I)
        searchObj2 = re.search(r'\(.+\)', text, re.M | re.I)
        if searchObj1:
            text = searchObj1.group().strip()
            new_text = text.replace(text, '').strip()

        if searchObj2:
            text = searchObj2.group().strip()
            new_text = text.replace(text, '').strip()

        return new_text
