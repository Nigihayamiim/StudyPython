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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
            "Cookie": "__stu=GGCHRWa5AHEg9ihX; 3AB9D23F7A4B3C9B=NTCZJ5MF6UE4MSMOZOLRHUKK57ORYC4THE6XYJGB7IQKEM57AQ5RBC7A25UEVW26Y4WLE3P3LXC5RMDDPTPKUFXA5Y; __jdv=59982123|baidu-search|t_262767352_baidusearch|cpc|159753633108_0_c630d82876644627bcf96a743a64378c|1591952888278; thor=C9C2876A4E30A11E064E419A89F53AB28B7806901D27425274D2264F8558349063B42A42B899747D88BCE217BE4216A32C14C6A8090DF3A96E38E0B1C9CFF7B362E8B3D2173215D7249AAEFA087B969E9C97748B3193069E9838097D893B938634F4CD6AEB2C15B0C181567987C1C701C7DED99D89E1618D75FEB7084EE5D13E6F523D23E9E4B0486BC962090ACE592E9F53F92D62BD46C0C939F509E582625B; pin=jd_ZpYJXyLqEWnv; unick=jd_ZpYJXyLqEWnv; __sts=GGCHRWa5AHEg9ihX|Wa5LFSHC9Gj; __jda=197855408.1591780348369911455505.1591780348.1592631533.1592724421.13; __jdc=197855408; JSESSIONID=DE912009F26A50A823F191038D2B4E23.s1"
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
                # "beginTime": begin_time,
                # "endTime": end_time,
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
                    r'style="color.*?">(.*?)</div>',
                    info)
                a = len(status)

                for sta in status:
                    s = str(sta)
                    b = len(s)

                if (s != "下单") & (s != "揽件再取") & (b != 0):

                    cursor.execute(sql_selectweight, [tknum])
                    order_weights = cursor.fetchall()
                    real_weights = re.findall(r'</b>重量：(.*?) kg</p>', info)

                    for order_weight in order_weights:
                        for o in order_weight:
                            ow = float(o)
                    for real_weight in real_weights:
                        rw = float(real_weight)

                    chazhi = rw - ow

                    cursor.execute(sql_selectordertime, [tknum])
                    order_time = cursor.fetchall()

                    if chazhi > 0:
                        cursor.execute(sql_setcheckweight, [tknum, order_weight, real_weight, chazhi, s, order_time])
                        cursor.execute(sql_updatecheck, [tknum])
                        print("已经检查到第"+str(num)+"条为超重，单号为：" + tknum[0])
                        num += 1
                    elif chazhi < -1 :
                        cursor.execute(sql_setcheckweight, [tknum, order_weight, real_weight, chazhi, s, order_time])
                        cursor.execute(sql_updatecheck, [tknum])
                        print("已经检查到第" + str(num) + "条为少重，单号为：" + tknum[0])
                        num += 1

                    else:
                        cursor.execute(sql_updatecheck, [tknum])
                        print("已经检查到第" + str(num) + "条为正常，单号为：" + tknum[0])
                        num += 1
                elif len(s) == 0:
                    cursor.execute(sql_updatecheck, [tknum])
                    print(str(num) + "条单号被删除了，单号为：" + tknum[0])
                    num += 1
                else:
                    print(str(num) + "条还没出单呢！，单号为：" + tknum[0])
                    num += 1

        client.commit()

if __name__ == '__main__':

    JD_url = "https://biz-wb.jdwl.com/business/waybillmanage/toDeliveryDetail"
    tracking_numbers = Queue()



    # begin_time = "2020-06-13 00:00:00"
    # end_time = "2020-06-13 23:59:59"


    client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
    cursor = client.cursor()

    sql_setcheckweight = 'insert ignore into CheckWeight_huabei(tknum,order_weight,real_weight,over_weight,status,order_time) values (%s, %s, %s, %s, %s, %s)'
    sql_selectnumbers = 'select tknum from OrderWeight_huabei where ischeck = "0"'
    sql_selectweight = 'select weight from OrderWeight_huabei where tknum = %s'
    sql_updatecheck = 'update OrderWeight_huabei set ischeck = "1" where tknum = %s'
    sql_updateNonum = 'update OrderWeight_huabei set ischeck = "无单号" where tknum = %s'
    sql_selectordertime = 'select order_time from OrderWeight_huabei where tknum = %s'

    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()
    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)


    crawl1 = CrawlInfo1(tracking_numbers, JD_url)
    crawl1.start()
    crawl1.join()


    cursor.close()
    client.close()
