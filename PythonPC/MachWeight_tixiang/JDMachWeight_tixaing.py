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
            "Cookie": "__stu=EDGESWa58EOuBAy3; 3AB9D23F7A4B3C9B=LWF5KQ5X4FZZDHIUUU45XC7F3O4I3HJKJ6QXJABGQBIZQWCIEWDOOXS3VDEJG5DBPV4YFQ4DKI32NYSNCWYZ3SSYTY; __jdv=59982123|direct|-|none|-|1595656673572; __sts=EDGESWa58EOuBAy3|Wa6RKeiEKZq; thor=B312B8A284476B56CAD34D789FE505764D9AC2D3D17605B0842A9AC253A01A367E0B00D9211C69EDBFC84DC95F67D13175A100A65F7F839E6488937DC13D61A838AD293D2F2319A5B15D6A1A15191D697E09C124B6E4F936F86B1B8B9AA08199D465E5C1891085FF6D7CBF82DCB057FC6B32D82D4A7C3607EC5B464ACE334BC5AC7D2EFF6E7E691C81BE7A071C666F8D4A5C8C1E7D0816410A9CFE03FCA760BD; pin=jd_EyrEhvUqbreC; unick=jd_EyrEhvUqbreC; __jda=197855408.15915962939721888410676.1591596294.1595768443.1595853051.67; __jdc=197855408; __jdb=197855408.9.15915962939721888410676|67.1595853051; JSESSIONID=59347483D09D207D9432C3707C5F6338.s1"
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

                if (s != "下单") & (s != "揽件再取") & (s != "客户取消") & (s != "终止揽收") & (b != 0):

                    cursor.execute(sql_selectweight, [tknum])
                    order_weights = cursor.fetchall()
                    real_weights = re.findall(r'</b>重量：(.*?) kg</p>', info)

                    for order_weight in order_weights:
                        for o in order_weight:
                            ow = o
                    for real_weight in real_weights:
                        rw = float(real_weight)

                    chazhi = rw - ow

                    cursor.execute(sql_selectordertime, [tknum])
                    order_time = cursor.fetchall()

                    cursor.execute(sql_selectorderper, [tknum])
                    order_per = cursor.fetchall()

                    if chazhi > 0:
                        cursor.execute(sql_setcheckweight, [tknum, ow, rw, chazhi, s, order_time, order_per])
                        cursor.execute(sql_updatechaozhong, [tknum])
                        print("已经检查到第" + str(num) + "条为超重，单号为：" + tknum[0])
                        num += 1
                    elif chazhi < -1:
                        cursor.execute(sql_setcheckweight, [tknum, ow, rw, chazhi, s, order_time, order_per])
                        cursor.execute(sql_shaozhong, [tknum])
                        print("已经检查到第" + str(num) + "条为少重，单号为：" + tknum[0])
                        num += 1

                    else:
                        cursor.execute(sql_zhengchang, [tknum])
                        print("已经检查到第" + str(num) + "条为正常，单号为：" + tknum[0])
                        num += 1
                elif len(s) == 0:
                    cursor.execute(sql_wudanhao, [tknum])
                    print(str(num) + "条单号被删除了，单号为：" + tknum[0])
                    num += 1
                elif s == "终止揽收":
                    cursor.execute(sql_zhongzholanshou, [tknum])
                    print("已经检查到第" + str(num) + "条为终止揽收，单号为：" + tknum[0])
                    num += 1
                elif s == "客户取消":
                    cursor.execute(sql_kehuquxiao, [tknum])
                    print("已经检查到第" + str(num) + "条为客户取消，单号为：" + tknum[0])
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

    sql_setcheckweight = 'insert ignore into CheckWeight_tixiang(tknum,order_weight,real_weight,over_weight,status,order_time, order_per) values (%s, %s, %s, %s, %s, %s, %s)'
    sql_selectnumbers = 'select tknum from OrderWeight_tixiang where ischeck = "0" and order_per = "小强-提象"'
    sql_selectweight = 'select weight from OrderWeight_tixiang where tknum = %s'
    sql_updatechaozhong = 'update OrderWeight_tixiang set ischeck = "超重" where tknum = %s'
    sql_shaozhong = 'update OrderWeight_tixiang set ischeck = "少重" where tknum = %s'
    sql_zhengchang = 'update OrderWeight_tixiang set ischeck = "正常" where tknum = %s'
    sql_zhongzholanshou = 'update OrderWeight_tixiang set ischeck = "终止揽收" where tknum = %s'
    sql_kehuquxiao = 'update OrderWeight_tixiang set ischeck = "客户取消" where tknum = %s'
    sql_wudanhao = 'update OrderWeight_tixiang set ischeck = "无单号" where tknum = %s'
    sql_selectordertime = 'select order_time from OrderWeight_tixiang where tknum = %s'
    sql_selectorderper = 'select order_per from OrderWeight_tixiang where tknum = %s'

    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()
    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)


    crawl1 = CrawlInfo1(tracking_numbers, JD_url)
    crawl1.start()
    crawl1.join()


    cursor.close()
    client.close()