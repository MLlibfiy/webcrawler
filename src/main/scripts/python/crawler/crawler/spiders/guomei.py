# encoding=utf-8

import scrapy

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
        #"cookie": "uid=CjozKFxlXH2ZbFGrnug1Ag==; __clickidc=130932891350146685; __c_visitor=130932891350146685; atgregion=21010100%7C%E4%B8%8A%E6%B5%B7%E4%B8%8A%E6%B5%B7%E5%B8%82%E9%BB%84%E6%B5%A6%E5%8C%BA%E5%8D%8A%E6%B7%9E%E5%9B%AD%E8%B7%AF%E8%A1%97%E9%81%93%7C21010000%7C21000000%7C210101001; __gma=ffb8de7.1755752503971.1550146685864.1550146685864.1550146685864.1; __gmc=ffb8de7; __gmv=1755752503971.1550146685864; sajssdk_2015_cross_new_user=1; cartnum=0_0-1_0; s_cc=true; gpv_p22=no%20value; DSESSIONID=1d811a80d7da4d2b90aedb67629d0603; _idusin=78789180386; _smt_uid=5c655c81.16780b9a; s_ev13=%5B%5B'sem_baidu_pinpai_yx_pc_bt'%2C'1550146690246'%5D%5D; route=a4740778113c5452684f57d9d18e1433; compare=; _index_ad=0; isnew=865072697836.1550146693046; asid=fc613e0869df4ddc544027df4550d853; gradeId=-1; gpv_pn=no%20value; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22168ebf14bc05a-0a4db6e7ec54c-b781636-1049088-168ebf14bc165%22%2C%22%24device_id%22%3A%22168ebf14bc05a-0a4db6e7ec54c-b781636-1049088-168ebf14bc165%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22_latest_cmpid%22%3A%22sem_baidu_pinpai_yx_pc_bt%22%7D%7D; proid120517atg=%5B%229140127825-1130602307%22%5D; _jzqco=%7C%7C%7C%7C%7C1.415178692.1550147528883.1550147556186.1550147563586.1550147556186.1550147563586.0.0.0.4.4; __gmz=ffb8de7|sem_baidu_pinpai_yx_pc_bt|-|sem|-|1iXOnj0V4CAF|-|1755752503971.1550146685864|dc-1|1550146685866; __gmb=ffb8de7.17.1755752503971|1.1550146685864; __xsptplusUT_194=1; __xsptplus194=194.1.1550146691.1550148037.15%232%7Csp0.baidu.com%7C%7C%7C%25E5%259B%25BD%25E7%25BE%258E%7C%23%23_LUjvH5uI7CJ76N169bc-RDECL2K-jmi%23; s_getNewRepeat=1550148050537-New; s_sq=gome-prd%3D%2526pid%253Dhttps%25253A%25252F%25252Fsearch.gome.com.cn%25252Fsearch%25253Fquestion%25253D%252525E6%25252589%2525258B%252525E6%2525259C%252525BA%252526searchType%25253Dgoods%252526search_mode%25253Dnormal%252526reWrite%25253Dtrue%2526oid%253Dfunctiononclick(event)%25257Bjavascript%25253AdoPageNumSearch(2)%25253Breturnfalse%25253B%25257D%2526oidt%253D2%2526ot%253DA; s_ppv=-%2C93%2C17%2C7129; plasttime=1550148057",
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
        # content = json.loads(response.text[response.text.find('(')+1:-2])
        # response.text 获取响应体
        # 转换成json
        # for each in response.xpath("//li[@class='gl-item']"):
        print(response.text)

    # 最后调用的方法
    def closed(self, reason):
        print("结束")
