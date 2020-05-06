import re
from queue import Queue
from threading import Thread
from time import sleep
from random import randint
import requests
from fake_useragent import UserAgent


class CrawlInfo1(Thread):
    def __init__(self, url_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome,
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNTg5MjIzNjAwLCJpYXQiOjE1ODg2Njc1NzUsImlkIjoxMTM3MjZ9.4hew7o-Hf-q8xDLX2xSvRIcHbUcQhBXqJQQlQdCQXPk"
        }
        proxies = {
            "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
            "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
        }

        with open("../day01/商品id2.txt", "a", encoding="utf-8") as f:
            num = 1
            while not self.url_queue.empty():
                response = requests.get(self.url_queue.get(), proxies=proxies, headers=headers)
                if response.status_code == 200:
                    response.encoding = "utf-8"
                    info = response.text
                    # print(info)
                    infos = re.findall(r'"promotion_id":"(\d{19})"', info)
                    for shop_id in infos:
                        f.write(shop_id + "\n")
                        shop_url_queue.put(base_shop_url.format(shop_id))
                    print("第" + str(num) + "页")
                    num += 1


class CrawlInfo2(Thread):
    def __init__(self, shop_url_queue, filename,  start_no):
        Thread.__init__(self)
        self.shop_url_queue = shop_url_queue
        self.filename = filename
        self.start_no = start_no

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        proxies = {
            "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
            "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
        }
        with open(self.filename, "a", encoding="utf-8") as f:
            num = 1
            count = 1
            while not self.shop_url_queue.empty():
                shop_url = self.shop_url_queue.get()
                response = requests.get(shop_url, headers=headers, proxies=proxies)
                code = response.status_code
                print("这是第"+str(count)+"条数据,地址为:"+shop_url)
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
            print(str(self.start_no)+"页的内容搜集完毕")

if __name__ == '__main__':
    base_url = "https://api-service.chanmama.com/v1/home/rank/yesterdayHotRank?category=&page={}&size=50&commission_rate=&date=2020-05-05"
    base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
    filename = "2020-4-30的内容.txt"
    start_No = 59
    while True:
        print("开始咯!")
        url_queue = Queue()
        shop_url_queue = Queue()
        url_queue.put(base_url.format(start_No))

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
        if shop_url_queue.empty():
            print("第"+str(start_No)+"没有数据了")
            break
        crawl2 = CrawlInfo2(shop_url_queue, filename, start_No)
        crawl2.start()
        crawl2.join()
        start_No += 1
        sleep(randint(1, 5))

