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
            "Cookie": "__stu=GGCHRWa5AHEg9ihX; 3AB9D23F7A4B3C9B=NTCZJ5MF6UE4MSMOZOLRHUKK57ORYC4THE6XYJGB7IQKEM57AQ5RBC7A25UEVW26Y4WLE3P3LXC5RMDDPTPKUFXA5Y; __jdv=59982123|baidu-search|t_262767352_baidusearch|cpc|159753633108_0_c630d82876644627bcf96a743a64378c|1591952888278; thor=12467F15FC83A299A0BBE831A76BB0D851AFDDFAD3447C608CE75A416493F630E9D749152C73BBE29EA9B04A64891B54105115D0440EAFA237BD7A2854A0465A0BCBDD53B14458A0CA34621C1D7B8CC0DC90372C8F011A26273D30CDF63F8B1A25F2F1AA6583588E8FD43673DCEEC4296CFE791E7F2F3ACDD51F2EAE6BC3220A377E73671C2BEF811B6C571A2EF92382F941247CF5B2BDA2B421D38FCF1755C9; pin=jd_ceRrROOyRMml; unick=jd_ceRrROOyRMml; __sts=GGCHRWa5AHEg9ihX|Wa5NKh702WK; __jda=197855408.1591780348369911455505.1591780348.1592742612.1592916094.15; __jdc=197855408; __jdb=197855408.4.1591780348369911455505|15.1592916094; JSESSIONID=E2289480A94FABC2F0588EE4C24D704E.s1"
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
                    client.commit()
                    real_weights = re.findall(r'</b>重量：(.*?) kg</p>', info)

                    for order_weight in order_weights:
                        for o in order_weight:
                            ow = float(o)
                    for real_weight in real_weights:
                        rw = float(real_weight)

                    chazhi = rw - ow

                    cursor.execute(sql_selectordertime, [tknum])
                    order_time = cursor.fetchall()
                    client.commit()

                    if chazhi > 0:
                        cursor.execute(sql_setcheckweight, [tknum, order_weight, real_weight, chazhi, s, order_time])
                        cursor.execute(sql_updatecheck, [tknum])
                        client.commit()
                        print("已经检查到第"+str(num)+"条为超重，单号为：" + tknum[0])
                        num += 1
                    elif chazhi < -1 :
                        cursor.execute(sql_setcheckweight, [tknum, order_weight, real_weight, chazhi, s, order_time])
                        cursor.execute(sql_updatecheck, [tknum])
                        client.commit()
                        print("已经检查到第" + str(num) + "条为少重，单号为：" + tknum[0])
                        num += 1

                    else:
                        cursor.execute(sql_updatecheck, [tknum])
                        client.commit()
                        print("已经检查到第" + str(num) + "条为正常，单号为：" + tknum[0])
                        num += 1
                elif len(s) == 0:
                    cursor.execute(sql_updatecheck, [tknum])
                    client.commit()
                    print(str(num) + "条单号被删除了，单号为：" + tknum[0])
                    num += 1
                else:
                    print(str(num) + "条还没出单呢！，单号为：" + tknum[0])
                    num += 1

if __name__ == '__main__':

    JD_url = "https://biz-wb.jdwl.com/business/waybillmanage/toDeliveryDetail"
    tracking_numbers = Queue()



    # begin_time = "2020-06-13 00:00:00"
    # end_time = "2020-06-13 23:59:59"


    client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
    cursor = client.cursor()

    sql_setcheckweight = 'insert ignore into CheckWeight_new3(tknum,order_weight,real_weight,over_weight,status,order_time) values (%s, %s, %s, %s, %s, %s)'
    sql_selectnumbers = 'select tknum from OrderWeight_new3 where ischeck = "0"'
    sql_selectweight = 'select weight from OrderWeight_new3 where tknum = %s'
    sql_updatecheck = 'update OrderWeight_new3 set ischeck = "1" where tknum = %s'
    sql_updateNonum = 'update OrderWeight_new3 set ischeck = "无单号" where tknum = %s'
    sql_selectordertime = 'select order_time from OrderWeight_new3 where tknum = %s'

    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()
    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)


    crawl1 = CrawlInfo1(tracking_numbers, JD_url)
    crawl1.start()
    crawl1.join()


    cursor.close()
    client.close()
