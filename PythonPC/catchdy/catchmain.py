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
            "Cookie": "_ga=GA1.2.1891294568.1587479976; __gads=ID=196a438dbf4084b2:T=1587480069:S=ALNI_MY-q1HznH1BF4_h56rL3jj0auybag; Hm_lvt_09720a8dd79381f0fd2793fad156ddfa=1587958221,1588039492,1588044735,1588166538; _gid=GA1.2.530615551.1588166539; XSRF-TOKEN=eyJpdiI6IlFDQjJmTThQSDBSM1RXK3ZDcGN3Rnc9PSIsInZhbHVlIjoiM25HWlpPU2l3UEZpOWdPM1lSR0huMWRYbnEyQlZQUGpyeVdOdVk0a1N6b0hlenNUMzVGZ1NaMEdiRUJGa3NNVSIsIm1hYyI6IjA0ZDEzOTMxYzA4MDkzOWUxYWUwODFhZGRhYjNlZmVhNjJiZDA1NDAwMTgzMGUyZGQzNWQ4MzU4YmFhMTg4Y2IifQ%3D%3D; toobigdata_session=eyJpdiI6IlJjZTk4SzhmdnZMUkRkaXNTSU9jeGc9PSIsInZhbHVlIjoiVTcyckpJcVwvbTFMUUp3cU56bmpyOFpZcFNNZGc0cjFHU2JQMnNJR09EK0pQUHRBTTRpNW83ZnkyKzZCQk96K1MiLCJtYWMiOiIwN2MxOWI5NjIwODNjMWU2Y2YwNzFlYzU4NjA3ZDg3MDQ0NGI1OTRjODNjNzNlNzcwZGVhZTk0NzFhMzFhMzUxIn0%3D; Hm_lpvt_09720a8dd79381f0fd2793fad156ddfa=1588170667; Hm_cv_09720a8dd79381f0fd2793fad156ddfa=1*email*312154402%40qq.com!*!*!1*role*free; _gat_gtag_UA_8981755_3=1",
            "User-Agent": UserAgent().chrome,
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
                infos = re.findall(r'<a href="/douyin/promotion/g/(33.*)" target="_blank">', info)
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
        with open("商家信息.txt", "a", encoding="utf-8") as f:
            while not self.shop_url_queue.empty():
                response = requests.get(self.shop_url_queue.get(), proxies=proxies, headers=headers)
                if response.status_code == 200:
                    response.encoding = "utf-8"
                    shop = response.text
                    shop_name = re.findall(r'"shop_name":"([\u4e00-\u9fa5]+)', shop)
                    shop_tel = re.findall(r'"shop_tel":"(\d+)', shop)
                    product_id = re.findall(r'"product_id":"(\d+)', shop)
                    f.write(product_id[0] + "\t" + shop_tel[0] + "\n")


if __name__ == '__main__':
    base_url = "https://toobigdata.com/douyin/promotions?page={}"
    base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
    url_queue = Queue()
    shop_url_queue = Queue()
    for pn in range(1, 2):
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
    #     crawl2 = CrawlInfo1(url_queue)
    #     crawl2.start()

    crawl1 = CrawlInfo1(url_queue)
    crawl1.start()
    crawl1.join()
    crawl2 = CrawlInfo1(url_queue)
    crawl2.start()