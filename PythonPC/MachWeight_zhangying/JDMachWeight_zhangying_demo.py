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
import pymysql as pymysql
import time
import tkinter as tk

from PythonPC.MachWeight_tixiang.forExcel import write_excel
from PythonPC.MachWeight_zhangying.choseDate import datepicker


def run():
    cookie = e.get()
    if var.get() == "张英":
        sql_setcheckweight = 'insert ignore into CheckWeight_zhangying (tknum,order_weight,real_weight,over_weight,status,order_time, order_per) values (%s, %s, %s, %s, %s, %s, %s)'
        sql_selectnumbers = 'select tknum from OrderWeight_zhangying where ischeck = "0" and order_per = "张英2"'
        sql_selectweight = 'select weight from OrderWeight_zhangying where tknum = %s'
        sql_updatechaozhong = 'update OrderWeight_zhangying set ischeck = "超重" where tknum = %s'
        sql_shaozhong = 'update OrderWeight_zhangying set ischeck = "少重" where tknum = %s'
        sql_zhengchang = 'update OrderWeight_zhangying set ischeck = "正常" where tknum = %s'
        sql_zhongzholanshou = 'update OrderWeight_zhangying set ischeck = "终止揽收" where tknum = %s'
        sql_kehuquxiao = 'update OrderWeight_zhangying set ischeck = "客户取消" where tknum = %s'
        sql_wudanhao = 'update OrderWeight_zhangying set ischeck = "无单号" where tknum = %s'
        sql_selectordertime = 'select order_time from OrderWeight_zhangying where tknum = %s'
        sql_selectorderper = 'select order_per from OrderWeight_zhangying where tknum = %s'
        sql_realweight = 'select * from CheckWeight_zhangying where check_time like %s'
    elif var.get() == "橘子君":
        sql_setcheckweight = 'insert ignore into CheckWeight_juzijun (tknum,order_weight,real_weight,over_weight,status,order_time, order_per) values (%s, %s, %s, %s, %s, %s, %s)'
        sql_selectnumbers = 'select tknum from OrderWeight_juzijun where ischeck = "0" and order_per = "小强-橘子君"'
        sql_selectweight = 'select weight from OrderWeight_juzijun where tknum = %s'
        sql_updatechaozhong = 'update OrderWeight_juzijun set ischeck = "超重" where tknum = %s'
        sql_shaozhong = 'update OrderWeight_juzijun set ischeck = "少重" where tknum = %s'
        sql_zhengchang = 'update OrderWeight_juzijun set ischeck = "正常" where tknum = %s'
        sql_zhongzholanshou = 'update OrderWeight_juzijun set ischeck = "终止揽收" where tknum = %s'
        sql_kehuquxiao = 'update OrderWeight_juzijun set ischeck = "客户取消" where tknum = %s'
        sql_wudanhao = 'update OrderWeight_juzijun set ischeck = "无单号" where tknum = %s'
        sql_selectordertime = 'select order_time from OrderWeight_juzijun where tknum = %s'
        sql_realweight = 'select * from CheckWeight_juzijun where check_time like %s'
        sql_selectorderper = 'select order_per from OrderWeight_juzijun where tknum = %s'

    client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
    cursor = client.cursor()

    tracking_numbers = Queue()
    cursor.execute(sql_selectnumbers)
    select_numbers = cursor.fetchall()

    # begin_time = "2020-06-13 00:00:00"
    # end_time = "2020-06-13 23:59:59"

    for tk_num in select_numbers:
        tracking_numbers.put(tk_num)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
        "Cookie": cookie
    }
    proxies = {
        "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
        "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
    }

    JD_url = "https://biz-wb.jdwl.com/business/waybillmanage/toDeliveryDetail"

    num = 1
    while not tracking_numbers.empty():

        tknum = tracking_numbers.get()

        form_data = {
            "deliveryI_h": tknum,
            # "beginTime": begin_time,
            # "endTime": end_time,
            "detailDeliveryId": tknum
        }

        try:
            response = requests.post(JD_url, headers=headers, data=form_data)
        except Exception:
            print("第" + str(num) + "页数据出现超时,尝试再次连接")
            response = requests.post(JD_url, headers=headers, data=form_data)
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

    cursor.close()
    client.close()

    print("核重完毕！")


    date = time.strftime("%Y-%m-%d", time.localtime())
    dates = date + "%"
    filename = date + var.get() + "全国超重少重统计.xls"

    conn = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                           db='JDWL')
    cursor = conn.cursor()
    cursor.execute(sql_realweight, [dates])
    datas = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    write_excel(datas, filename, date)


window = tk.Tk()
window.title("核重")
window.geometry("500x260")

tk.Label(window, text='请输入cookie值:').place(x=20, y=20)
e = tk.Entry(window, width=38)
e.place(x=130, y=20)



var = tk.StringVar()
var.set(0)

l = tk.Label(window, bg='yellow', width=20, text='请选择需要核重的账号')
l.place(x=190, y=90)


def print_selection():
    l.config(text='核重账号:' + var.get())


r1 = tk.Radiobutton(window, text='张英', variable=var, value='张英', command=print_selection)
r1.place(x=200, y=120)
r2 = tk.Radiobutton(window, text='橘子君', variable=var, value='橘子君', command=print_selection)
r2.place(x=200, y=150)


b = tk.Button(window, text='开始核重', width=15, height=2, command=run)
b.place(x=200, y=180)

# tk.Label(window, text="显示", bg="green", font=("Arial", 12), width=5, height=1).place(x=200, y=250)
# EditText = tk.Text(window, width=56, height=12).place(x=50, y=300)
# def printtext():
#      EditText.insert(1.0, run())
# EditText.grid(row=2, column=3)
window.mainloop()

# import tkinter as tk
#
# root = tk.Tk()
# root.title("how to do ")
# root.geometry('500x300')
# tk.Label(root, text="显示", bg="green", font=("Arial", 12), width=5, height=1).place(x=20, y=30)
#
#
# def printtext():
#     EditText.insert(1.0, A())
#
#
# def A():
#     if 2 > 3:
#         return "句子1"
#     elif 2 < 0:
#         return "句子2"
#     else:
#         return "句子3"
#
#
# EditText = tk.Text(root, width=20, height=10)
# EditText.grid(row=2, column=3)
# btn_test = tk.Button(root, text="按钮", command=printtext, width=5, height=2)
#
# btn_test.place(x=200, y=60)
#
# root.mainloop()
