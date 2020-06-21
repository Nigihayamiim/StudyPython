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
            "Cookie": "__stu=GGCHRWa5AHEg9ihX; 3AB9D23F7A4B3C9B=NTCZJ5MF6UE4MSMOZOLRHUKK57ORYC4THE6XYJGB7IQKEM57AQ5RBC7A25UEVW26Y4WLE3P3LXC5RMDDPTPKUFXA5Y; __jdv=59982123|baidu-search|t_262767352_baidusearch|cpc|159753633108_0_c630d82876644627bcf96a743a64378c|1591952888278; __sts=GGCHRWa5AHEg9ihX|Wa5LFSHC9Gj; thor=3678ADE2F618CDD027CE50B8164B4D06638CEFA64954D1CF2B2DF76B5F16E0BF532993EF0582B82356B84F50CAF070748F988F668671F47C9EAEB26385B73DAA69426A6D5B4336FE8B2D66B17358A7A196534794CABEACC458D0A4F02640BC3FF15062CE83BC23E0979009E25DDB8F212FFF5247346A3F30CC615E4F009A73E4C85EFD1A215A83E1B4B41C4880665B1456EC9B798E6C6C88F199AF6C9093B96C; pin=jd_41fe9e06f3ef1; unick=jd_41fe9e06f3ef1; __jda=197855408.1591780348369911455505.1591780348.1592724421.1592742612.14; __jdc=197855408; __jdb=197855408.6.1591780348369911455505|14.1592742612; JSESSIONID=961D940063237753462D2F7A0D0D56C3.s1"
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

    sql_setcheckweight = 'insert ignore into CheckWeight(tknum,order_weight,real_weight,over_weight,status,order_time) values (%s, %s, %s, %s, %s, %s)'
    sql_selectnumbers = 'select tknum from OrderWeight where ischeck = "0"'
    sql_selectweight = 'select weight from OrderWeight where tknum = %s'
    sql_updatecheck = 'update OrderWeight set ischeck = "1" where tknum = %s'
    sql_updateNonum = 'update OrderWeight set ischeck = "无单号" where tknum = %s'
    sql_selectordertime = 'select order_time from OrderWeight where tknum = %s'

    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()
    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)


    crawl1 = CrawlInfo1(tracking_numbers, JD_url)
    crawl1.start()
    crawl1.join()


    cursor.close()
    client.close()
