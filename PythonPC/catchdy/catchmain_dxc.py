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
            "Cookie": "_ga=GA1.2.1891294568.1587479976; __gads=ID=196a438dbf4084b2:T=1587480069:S=ALNI_MY-q1HznH1BF4_h56rL3jj0auybag; _gid=GA1.2.530615551.1588166539; Hm_lvt_09720a8dd79381f0fd2793fad156ddfa=1588219809,1588221051,1588227194,1588231131; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImVUdGJTdjU0ZmRcL09LWWZ5eHFFRVF3PT0iLCJ2YWx1ZSI6ImNWakJ0NE82YWU2a0o3NUNVNHIwcnFFeDdiY1BVNGxGTm9kVXA0Q3JoZTJPUVk4Sk9ocExCVG9SVFRRR1p6bm1STVwvV3BNZW5cL0tiUklZM3FGTmtiKzZ4Y0lOdWNDbUs2b3ZcL2JSanV2RnRVZm9YeWozc21ZQUk0MytrYlJzWEM3Q09IdmhZUURcLzV1aUJCa0tObTF0WGc9PSIsIm1hYyI6IjlkNzkzODYxNGI2ZWUxZjlmZjA1MmYxN2RlM2Y0OTIwZDFhZDBhOTljZGM0NTIzYTIxZWJjYjBjZjhhN2YzZWIifQ%3D%3D; XSRF-TOKEN=eyJpdiI6ImJmKzhscE94blhBdDFwSUhPa1wvSzJ3PT0iLCJ2YWx1ZSI6IldrQ3lPblQ0YVUrSkp5cWxJR1JMWmI1VVhhQWlsczFONUdEQ0UwWFwvMVRaU1ZsUFNENjdPZ2R0R3k3QWRzRGlBIiwibWFjIjoiNDczMzMyNjA4ZGNkYjA0NzRlNjg2NDQ0ZDc2Y2RhOWNjNjMxNjk4ZjZhY2UwYWIwMmJlZTg2MjJlMWM0NWVmMCJ9; toobigdata_session=eyJpdiI6ImdEcnZjWDJ0QVVYMDdpemhTV2t6MEE9PSIsInZhbHVlIjoiK2lrV0ZjU00wXC8ycUNkVktYcnpzdEkrN1h0bFAxdUJWSkNYejB0R1NcL0NLakY2akN6SjdyOVlxZWRKQXk0OXc0IiwibWFjIjoiYWQ5ZDU5ODA3NTM1YzE4YmY0YzA1ZDg4YmQ1MmFiYTc0NjhhMzIyNWIxZTk2OWNkNjcwMTEwY2RjMDY0OGM1ZiJ9; Hm_lpvt_09720a8dd79381f0fd2793fad156ddfa=1588237124; Hm_cv_09720a8dd79381f0fd2793fad156ddfa=1*email*odgLGv-lhihzzW64F3LcP3Xc5JFg%40wechat.com!*!*!1*role*free; _gat_gtag_UA_8981755_3=1"
        }
        proxies = {
            "http": "http://117.88.176.145:3000"
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
    def __init__(self, shop_url_queue, filename):
        Thread.__init__(self)
        self.shop_url_queue = shop_url_queue
        self.filename = filename

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        proxies = {
            "http": "http://117.88.176.145:3000"
        }
        with open(self.filename, "a", encoding="utf-8") as f:
            num = 1
            while not self.shop_url_queue.empty():
                response = requests.get(self.shop_url_queue.get(), proxies=proxies, headers=headers)
                if response.status_code == 200:
                    response.encoding = "utf-8"
                    shop = response.text
                    shop_name = re.findall(r'"shop_name":"(.*?)"', shop)
                    shop_tel = re.findall(r'"shop_tel":"(1\d{10})', shop)
                    product_id = re.findall(r'"product_id":"(\d+)', shop)
                    if len(shop_tel):
                        f.write(shop_tel[0] + "\n")
                        print("已收集" + str(num) + "条数据")
                        num += 1


if __name__ == '__main__':
    base_url = "https://toobigdata.com/douyin/promotions?page={}"
    base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
    url_queue = Queue()
    shop_url_queue = Queue()
    start_no = 170
    filename = "2020-4-30_1-170的内容.txt"
    for pn in range(start_no, start_no+30):
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
    crawl2 = CrawlInfo2(shop_url_queue, filename)
    crawl2.start()
