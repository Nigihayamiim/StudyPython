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
            "Cookie": "__stu=EDGESWa58EOuBAy3; 3AB9D23F7A4B3C9B=LWF5KQ5X4FZZDHIUUU45XC7F3O4I3HJKJ6QXJABGQBIZQWCIEWDOOXS3VDEJG5DBPV4YFQ4DKI32NYSNCWYZ3SSYTY; __jdv=59982123|direct|-|none|-|1593002069616; thor=12467F15FC83A299A0BBE831A76BB0D851AFDDFAD3447C608CE75A416493F63000CA2F610BD8838B53B160DBA5BA9BB4C03228B77D2E0D5F53CFD9C24A8E42641A15FDB5E1F2861D9611FED25961E890D207F5327561C6618FA98D7CB6128AD8CB4344A8F4928C8610E6F9890D7FC286CC03A5CB92DE0F9076E4A93E28CAFB43ED6CEE7FC1936D6E2DA57CE7419CF1DE17EB2F68EB05BCCF70810D8716E03DC1; pin=jd_ceRrROOyRMml; unick=jd_ceRrROOyRMml; __sts=EDGESWa58EOuBAy3|Wa68L0l9IyZ; __jda=197855408.15915962939721888410676.1591596294.1594130273.1594213239.50; __jdc=197855408; __jdb=197855408.3.15915962939721888410676|50.1594213239; JSESSIONID=50A9870C309AE3951303CB77AB0442D2.s1"
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
