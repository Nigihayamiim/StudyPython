import re
from queue import Queue
from threading import Thread

import requests
from fake_useragent import UserAgent


class CrawlInfo1(Thread):
    def __init__(self, url_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome,
            "Cookie": "_ga=GA1.2.1891294568.1587479976; __gads=ID=196a438dbf4084b2:T=1587480069:S=ALNI_MY-q1HznH1BF4_h56rL3jj0auybag; _gid=GA1.2.530615551.1588166539; Hm_lvt_09720a8dd79381f0fd2793fad156ddfa=1588302176,1588303634,1588312427,1588324632; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImpXK1poZnFFQ3FIejJLclJaUEFwd3c9PSIsInZhbHVlIjoiREFoNTJwK3NNb2Q3UFBNS1FEdUhGbytwb0s1T25SeG12b2xoUVwveEE0S3VwdWUxVkRtK0tjY2FnK3RNWEtScWFibXRLSXJMWFZZeGN6bjFqWmFET3FLTUpIRmgyd2E4TzZmSE0xZGI2RytwN1wvQVVFeFNLeWRwNHgxXC85dzU3YkVFNHZmN3c2OVVPWWJWRXpKMTEyUGl3PT0iLCJtYWMiOiI1ZGY0OWI4MGMwMjE1MDk4ZTlmNDQ4MzEyMDA2N2ZhOGZmOWU5M2QwZDUxNDNmZmViODUxNTc0NmE2ODMxYmI4In0%3D; Hm_cv_09720a8dd79381f0fd2793fad156ddfa=1*email*luantao985544%40163.com!*!*!1*role*free; XSRF-TOKEN=eyJpdiI6ImpTMjNJWERTQWUzOEhNd01LVDdyMEE9PSIsInZhbHVlIjoiT2ZTM2E1RytIUmVBeFwvS2p4RSttVUlHWGUyNjlGY3V4cWNcL1NTeHoyTXoyazAxT0QwTkdzN3pRNHVyS3pQa1RuIiwibWFjIjoiNjVjODcxNzRiYjMyMmRlNjY3MjdiNDVlMWViNDY5ZmUyOTIxN2E2NmY2OTExNGI4YTMwM2NiZTdmMjFiMTNiMiJ9; toobigdata_session=eyJpdiI6IjRTbVdnVGFuSElnTkxjWnBGNzlcL0V3PT0iLCJ2YWx1ZSI6IjZQc1hhXC81TzVZdUdEZnBRSXphZit5WURcL2w4M3IrSmgrZ3hRZ0llOFJHVUc2OHJvZUM4d3lpaWNkUWkza2NPYyIsIm1hYyI6IjRiMzI3NDZhNzcyZjU5YzA3NmYyYzNhNjAyNjhkMDQ4NjM3ODYyYTg4ZGYxZmQ0Y2YzMWZkOWZjMDFiMTE3NDAifQ%3D%3D; Hm_lpvt_09720a8dd79381f0fd2793fad156ddfa=1588324695"

        }
        proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "http://127.0.0.1:1080"
        }
        num = 1
        while not self.url_queue.empty():
            response = requests.get(self.url_queue.get(), proxies=proxies, headers=headers)
            if response.status_code == 200:
                response.encoding = "utf-8"
                info = response.text
                # print(info)
                infos = re.findall(r'<div class="col-md-2">\s+<a href="/douyin/promotion/g/(\d{19})" target="_blank"',
                                   info)
                for shop_id in infos:
                    shop_url_queue.put(base_shop_url.format(shop_id))
                print("第" + str(num) + "页")
                num += 1


class CrawlInfo2(Thread):
    def __init__(self, shop_url_queue, filename, end_no, start_no):
        Thread.__init__(self)
        self.shop_url_queue = shop_url_queue
        self.filename = filename
        self.end_no = end_no
        self.start_no = start_no

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "http://127.0.0.1:1080"
        }
        with open(self.filename, "a", encoding="utf-8") as f:
            num = 1
            count = 1
            while not self.shop_url_queue.empty():
                shop_url = self.shop_url_queue.get()
                response = requests.get(shop_url, headers=headers, proxies=proxies)
                code = response.status_code
                print("这是第"+str(count)+"条数据,状态码为:"+str(code)+shop_url)
                count += 1
                if code == 200:
                    response.encoding = "utf-8"
                    shop = response.text
                    shop_name = re.findall(r'"shop_name":"(.*?)"', shop)
                    shop_tel = re.findall(r'"shop_tel":"(1\d{10})', shop)
                    product_id = re.findall(r'"product_id":"(\d+)', shop)
                    if len(shop_tel):
                        f.write(shop_tel[0] + "\n")
                        print("已收集" + str(num) + "条数据")
                        num += 1
            print(str(start_no)+"页到"+str(end_no)+"页的内容搜集完毕")

if __name__ == '__main__':
    base_url = "https://toobigdata.com/douyin/promotions?page={}"
    base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
    url_queue = Queue()
    shop_url_queue = Queue()
    start_no = 295
    end_no = start_no + 5
    filename = "2020-5-1_1-300的内容.txt"
    for pn in range(start_no, end_no):
        url_queue.put(base_url.format(pn))

    # crawl1_list = []
    # for i in range(0, 3):
    #     crawl1 = CrawlInfo1(url_queue)
    #     crawl1_list.append(crawl1)
    #     crawl1.start()
    # for crawl1s in crawl1_list:
    #     crawl1s.join()
    #
    # for i in range(0, 3):
    #     crawl2 = CrawlInfo2(shop_url_queue)
    #     crawl2.start()

    crawl1 = CrawlInfo1(url_queue)
    crawl1.start()
    crawl1.join()
    crawl2 = CrawlInfo2(shop_url_queue, filename, end_no, start_no)
    crawl2.start()
