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
            "Cookie": "__jdv=59982123|baidu-search|t_262767352_baidusearch|cpc|159753633089_0_571be123ec7f401fb0b2d0712790fc4c|1591597483412; __stu=EDGESWa58EOuBAy3; 3AB9D23F7A4B3C9B=LWF5KQ5X4FZZDHIUUU45XC7F3O4I3HJKJ6QXJABGQBIZQWCIEWDOOXS3VDEJG5DBPV4YFQ4DKI32NYSNCWYZ3SSYTY; thor=3678ADE2F618CDD027CE50B8164B4D06638CEFA64954D1CF2B2DF76B5F16E0BFEE61ACAD1E841CAD003DF753BE8E1399C55070BDE941DA90290E12E63328487B586D64674DF7A9879EA813B5A4C92673EFC39BF8F36408CE90A66AA60DCA628475377808898E7751896B89B16CF404C9C858EB3E1FD9B184DB90F4CFC5AC4E3A83FAF8F7AD5476D4B0C82F6284766475213376404C32CF6777B7B28862AF31CB; pin=jd_41fe9e06f3ef1; unick=jd_41fe9e06f3ef1; __sts=EDGESWa58EOuBAy3|Wa5DFLbErWG; __jda=197855408.15915962939721888410676.1591596294.1591952912.1592032744.8; __jdc=197855408; JSESSIONID=5E96294692B2F903ED8F595F53DA94CB.s1"
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



    begin_time = "2020-06-13 00:00:00"
    end_time = "2020-06-13 23:59:59"


    client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
    cursor = client.cursor()

    sql_setcheckweight = 'insert ignore into CheckWeight(tknum,order_weight,real_weight,status) values (%s, %s, %s, %s)'
    sql_selectnumbers = 'select tknum from OrderWeight where ischeck = "0"'
    sql_selectweight = 'select weight from OrderWeight where tknum = %s'
    sql_updatecheck = 'update OrderWeight set ischeck = "1" where tknum = %s'

    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()
    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)


    crawl1 = CrawlInfo1(tracking_numbers, JD_url)
    crawl1.start()
    crawl1.join()


    cursor.close()
    client.close()
