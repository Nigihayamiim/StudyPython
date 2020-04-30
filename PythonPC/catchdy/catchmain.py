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
            "Cookie": "_ga=GA1.2.1891294568.1587479976; __gads=ID=196a438dbf4084b2:T=1587480069:S=ALNI_MY-q1HznH1BF4_h56rL3jj0auybag; _gid=GA1.2.530615551.1588166539; Hm_lvt_09720a8dd79381f0fd2793fad156ddfa=1588044735,1588166538,1588172967,1588215561; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlFXVThqVFRCakxNTVV3RWdcL3JBWGNRPT0iLCJ2YWx1ZSI6Im5ia1daQnN2MGdIXC9DVlZuMmpOVE1nVWlCUGwya2VmMjIxN2h2bFlpWHFhMWprSTlCc29TZ0JUZmlCZXQ4WFNDN0dHYVhzQzl6U3Y3WkUrMGxqUnArZz09IiwibWFjIjoiYTAzZjVmNzk3ZjMyMDEzNmJiNGZlZjEzYmM3Y2EzNDc2YTRhMWI1ZjU1MzI1YzU5NjZlYzNmNDhlOGIyYjBmNCJ9; Hm_cv_09720a8dd79381f0fd2793fad156ddfa=1*email*odgLGvzSuPzOzCjPGPuVRmiQe9aQ%40wechat.com!*!*!1*role*free; _gat_gtag_UA_8981755_3=1; XSRF-TOKEN=eyJpdiI6IlBFc2I5ZFVoT3dyUW9IUDY3ZURIVEE9PSIsInZhbHVlIjoid1Z2VWhhbTdLOG04amhnRU9vOUFES0tTTHlzMUtyeVF4ZVhPUTNKYlNNOUpxcU1SQUtwYlRwUGp0YytrY2RtUyIsIm1hYyI6Ijc1OTM1ZWVhOTgwOWViNGUwMTM4YmI0ZTVlYTgxMDUzYzRmZjUzYWJiMDRlMTQ3MTk0NDA3OTQwMjVhNGE1YTgifQ%3D%3D; toobigdata_session=eyJpdiI6ImpUTlVNa2FNVmloYkV5bFJMZndFREE9PSIsInZhbHVlIjoiRTJaVk4rNDNnUiszemhRb3hCY0dvSUlQcnNkSWhsaGFua1Q1bUZFODBLQXZvSTYrNDllRDlXZWFVUlFKbHpQRCIsIm1hYyI6IjUyNWVhMmU1MWY3NGQ3NGE2ZGQ1ZWY2NzA3ODNiN2M4NzY3NDJlYmFmNjMwNzJlM2RmOTE0MGUwZjJkNDA0NDQifQ%3D%3D; Hm_lpvt_09720a8dd79381f0fd2793fad156ddfa=1588215738"
        }
        proxies = {
            "http": "http://117.88.176.145:3000"
        }

        while not self.url_queue.empty():
            response = requests.get(self.url_queue.get(), proxies=proxies, headers=headers)
            if response.status_code == 200:
                response.encoding = "utf-8"
                info = response.text
                # print(info)
                infos = re.findall(r'<a href="/douyin/promotion/g/(\d{19})" target="_blank">', info)
                for shop_id in infos:
                    shop_url_queue.put(base_shop_url.format(shop_id))


class CrawlInfo2(Thread):
    def __init__(self, shop_url_queue):
        Thread.__init__(self)
        self.shop_url_queue = shop_url_queue

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        proxies = {
            "http": "http://117.88.176.145:3000"
        }
        with open("商家信息3.txt", "a", encoding="utf-8") as f:
            while not self.shop_url_queue.empty():
                response = requests.get(self.shop_url_queue.get(), proxies=proxies, headers=headers)
                if response.status_code == 200:
                    response.encoding = "utf-8"
                    shop = response.text
                    shop_name = re.findall(r'"shop_name":"(.*?)"', shop)
                    shop_tel = re.findall(r'"shop_tel":"(1\d+)', shop)
                    product_id = re.findall(r'"product_id":"(\d+)', shop)
                    if len(shop_tel):
                        f.write(shop_tel[0] + "\n")


if __name__ == '__main__':
    base_url = "https://toobigdata.com/douyin/promotions?page={}"
    base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
    url_queue = Queue()
    shop_url_queue = Queue()
    for pn in range(3, 10):
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
    crawl2 = CrawlInfo2(shop_url_queue)
    crawl2.start()