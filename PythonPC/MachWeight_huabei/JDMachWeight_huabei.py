import re
import warnings
from queue import Queue
from threading import Thread
from time import sleep
from random import randint

import pymysql as pymysql
import requests
from fake_useragent import UserAgent

from PythonPC.IntoExcel.forExcel import write_excel


class CrawlInfo1(Thread):
    def __init__(self, tracking_numbers, JD_url):
        Thread.__init__(self)
        self.tk_nums = tracking_numbers
        self.url = JD_url

    def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Cookie": "__stu=GGCHRWa5AHEg9ihX; 3AB9D23F7A4B3C9B=NTCZJ5MF6UE4MSMOZOLRHUKK57ORYC4THE6XYJGB7IQKEM57AQ5RBC7A25UEVW26Y4WLE3P3LXC5RMDDPTPKUFXA5Y; __jdv=59982123|baidu-search|t_262767352_baidusearch|cpc|159753633108_0_c630d82876644627bcf96a743a64378c|1591952888278; thor=C9C2876A4E30A11E064E419A89F53AB28B7806901D27425274D2264F85583490C3A657C3BCA753F4F61A56A97756EED2733AF31CC73F1EAD1C5A25A127AF074D634B47AECB7481E8718616752FE5D61C64DB4087BBC51B22D5246760F237F04996F804B2D12B7D5D625EACE3D33148B628A3600B2F8C1788B4BEA0892F4E7C5A53BCD150B18326911D765124E8D2367EA4585D986150FB4AE0E0F618B6994664; pin=jd_ZpYJXyLqEWnv; unick=jd_ZpYJXyLqEWnv; __sts=GGCHRWa5AHEg9ihX|Wa5DFNvCVKt; __jda=197855408.1591780348369911455505.1591780348.1591952884.1592032953.5; __jdc=197855408; JSESSIONID=DA378A706470D4ABBF2F4495D1632AB6.s1"
        }
        proxies = {
            "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
            "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
        }


        num = 1
        while not self.tk_nums.empty():

            tknum = self.tk_nums.get()

            form_data = {
                "deliveryI_h": tknum,
                "beginTime": begin_time,
                "endTime": end_time,
                "detailDeliveryId": tknum
            }

            try:
                response = requests.post(self.url,  headers=headers, data=form_data)
            except Exception:
                print("第"+str(num)+"页数据出现超时,尝试再次连接")
                response = requests.post(self.url,  headers=headers, data=form_data)
            if response.status_code == 200:
                response.encoding = "utf-8"
                info = response.text
                # print(info)
                status = re.findall(
                    r'style="color: #1997ff ">(.*?)</div>',
                    info)
                for sta in status:
                    s = str(sta)
                if s != "下单":

                    cursor.execute(sql_selectweight, [tknum])
                    order_weights = cursor.fetchall()
                    real_weights = re.findall(r'</b>重量：(.*?) kg</p>', info)

                    for order_weight in order_weights:
                        for o in order_weight:
                            ow = float(o)
                    for real_weight in real_weights:
                        rw = float(real_weight)

                    chazhi = rw - ow

                    if chazhi > 0 :
                        cursor.execute(sql_setcheckweight, [tknum, order_weight, real_weight, s])
                        cursor.execute(sql_updatecheck, [tknum])
                        client.commit()
                        print("已经检查到第"+str(num)+"条为超重")
                        num += 1
                    elif chazhi < -1 :
                        cursor.execute(sql_setcheckweight, [tknum, order_weight, real_weight])
                        cursor.execute(sql_updatecheck, [tknum])
                        client.commit()
                        print("已经检查到第" + str(num) + "条为少重")
                        num += 1
                    else:
                        cursor.execute(sql_updatecheck, [tknum])
                        client.commit()
                        print("已经检查到第" + str(num) + "条为正常")
                        num += 1

                else:
                    print("还没出单呢！")

if __name__ == '__main__':

    JD_url = "https://biz-wb.jdwl.com/business/waybillmanage/toDeliveryDetail"
    tracking_numbers = Queue()



    begin_time = "2020-06-06 00:00:00"
    end_time = "2020-06-13 23:59:59"

    client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
    cursor = client.cursor()

    sql_setcheckweight = 'insert ignore into CheckWeight_huabei(tknum,order_weight,real_weight,status) values (%s, %s, %s, %s)'
    sql_selectnumbers = 'select tknum from OrderWeight_huabei where ischeck = "0"'
    sql_selectweight = 'select weight from OrderWeight_huabei where tknum = %s'
    sql_updatecheck = 'update OrderWeight_huabei set ischeck = "1" where tknum = %s'

    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()
    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)


    crawl1 = CrawlInfo1(tracking_numbers, JD_url)
    crawl1.start()
    crawl1.join()


    cursor.close()
    client.close()
