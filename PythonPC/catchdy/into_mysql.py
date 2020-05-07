import re
import warnings
from queue import Queue
from threading import Thread
from time import sleep
from random import randint

import pymysql as pymysql
import requests
from fake_useragent import UserAgent


class CrawlInfo1(Thread):
    def __init__(self, url_queue):
        Thread.__init__(self)
        self.url_queue = url_queue

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome,
            "Cookie": "_ga=GA1.2.1891294568.1587479976; __gads=ID=196a438dbf4084b2:T=1587480069:S=ALNI_MY-q1HznH1BF4_h56rL3jj0auybag; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImpXK1poZnFFQ3FIejJLclJaUEFwd3c9PSIsInZhbHVlIjoiREFoNTJwK3NNb2Q3UFBNS1FEdUhGbytwb0s1T25SeG12b2xoUVwveEE0S3VwdWUxVkRtK0tjY2FnK3RNWEtScWFibXRLSXJMWFZZeGN6bjFqWmFET3FLTUpIRmgyd2E4TzZmSE0xZGI2RytwN1wvQVVFeFNLeWRwNHgxXC85dzU3YkVFNHZmN3c2OVVPWWJWRXpKMTEyUGl3PT0iLCJtYWMiOiI1ZGY0OWI4MGMwMjE1MDk4ZTlmNDQ4MzEyMDA2N2ZhOGZmOWU5M2QwZDUxNDNmZmViODUxNTc0NmE2ODMxYmI4In0%3D; _gid=GA1.2.2049799570.1588762378; Hm_cv_09720a8dd79381f0fd2793fad156ddfa=1*email*luantao985544%40163.com!*!*!1*role*free; Hm_lvt_09720a8dd79381f0fd2793fad156ddfa=1588594078,1588661206,1588762378,1588824209; XSRF-TOKEN=eyJpdiI6Ik1DcFwvNkFUMzBMcytYZXkzSFJKSlVRPT0iLCJ2YWx1ZSI6IlRLSHhwVGhqNCthM3BoMEZrOXpZMlU3WitDUVB4eEd1VThvZkdoNlpGYnk2M0ZoazB5TWVFRXlrNGZBZGJJTFEiLCJtYWMiOiI0MmFmODgzZTJjYjY3MjhhOTkxNzgxOWVmMzYxMWM1NzA1NzY0YzU1YjUzYmY3ZjM5YWE0ZTc1ZGUxZTRlMDkyIn0%3D; toobigdata_session=eyJpdiI6ImpcL1VVcjI3c3NJWUVFdm1Gc2JMS2xBPT0iLCJ2YWx1ZSI6Im5ybVR5bzdYc2tGYmdQODJKNk9YeHhJaG5WWkU0Y096STJZZWF3SVdlM2tZb280Y29zZ2tDdFdONlBENXNcL0dmIiwibWFjIjoiZTMzZTY5NjVlODk1Mjg1ZDgzYzg3OTM0YzExNjAxZjQxM2Q3NGM1MDljZTkxMGRhZjc0MjE2NjhiODE4NzUzMCJ9; Hm_lpvt_09720a8dd79381f0fd2793fad156ddfa=1588827435; _gat_gtag_UA_8981755_3=1"

        }
        proxies = {
            "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
            "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
        }

        num = 1
        while not self.url_queue.empty():
            try:
                response = requests.get(self.url_queue.get(), proxies=proxies, headers=headers)
            except Exception:
                print("第"+str(num)+"页数据出现超时,尝试再次连接")
                response = requests.get(self.url_queue.get(), proxies=proxies, headers=headers)
            if response.status_code == 200:
                response.encoding = "utf-8"
                info = response.text
                # print(info)
                infos = re.findall(
                    r'<div class="col-md-2">\s+<a href="/douyin/promotion/g/(\d{19})" target="_blank"',
                    info)
                for shop_id in infos:
                    result = cursor.execute(sql_goods_id, [shop_id])
                    if result:
                        shop_url_queue.put(base_shop_url.format(shop_id))
                print("第" + str(num) + "页")
                num += 1


class CrawlInfo2(Thread):
    def __init__(self, shop_url_queue, end_no, start_no):
        Thread.__init__(self)
        self.shop_url_queue = shop_url_queue
        self.end_no = end_no
        self.start_no = start_no

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        proxies = {
            "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
            "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
        }
        num = 1
        count = 1
        while not self.shop_url_queue.empty():
            shop_url = self.shop_url_queue.get()
            try:
                response = requests.get(shop_url, headers=headers, proxies=proxies)
            except Exception:
                print("第"+str(count)+"条数据出现超时,尝试再次连接")
                response = requests.get(shop_url, headers=headers, proxies=proxies)
            code = response.status_code
            print("这是第" + str(count) + "条数据,地址为:" + shop_url)
            sleep(randint(0, 1))
            count += 1
            if code == 200:
                response.encoding = "utf-8"
                shop = response.text
                shop_position = ''.join(re.findall(r'"product_province_name":"(.*?)"', shop))
                shop_id = ''.join(re.findall(r'"shop_id":"(.*?)"', shop))
                shop_name = ''.join(re.findall(r'"shop_name":"(.*?)"', shop))
                shop_tel = ''.join(re.findall(r'"shop_tel":"(.*?)"', shop))
                product_id = ''.join(re.findall(r'"product_id":"(.*?)"', shop))
                good_name = ''.join(re.findall(r'"name":"(.*?)"', shop))
                result = cursor.execute(sql_goods, [product_id, good_name, shop_id])
                if result:
                    print("成功添加了"+str(num)+"条数据")
                    cursor.execute(sql_shop, [shop_id, shop_name, shop_tel, shop_position])
                    client.commit()
                    num += 1
        print(str(start_no) + "页到" + str(end_no) + "页的内容搜集完毕")


if __name__ == '__main__':
    base_url = "https://toobigdata.com/douyin/promotions?page={}"
    base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
    client = pymysql.connect(host='106.53.192.189', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='shop')
    cursor = client.cursor()
    sql_goods = 'insert ignore into goods values (%s, %s, %s)'
    sql_shop = 'insert ignore into shop(shop_id,shop_name,shop_tel,shop_position) values (%s,%s,%s,%s)'
    sql_goods_id = 'insert ignore into goods_id values (%s)'

    warnings.filterwarnings("ignore")

    start_No = 349
    for i in range(1, 11):
        print("开始咯!")
        url_queue = Queue()
        shop_url_queue = Queue()
        start_no = start_No
        end_no = start_no + 5
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
        crawl2 = CrawlInfo2(shop_url_queue, end_no, start_no)
        crawl2.start()
        crawl2.join()
        start_No += 5
        sleep(randint(1, 5))
