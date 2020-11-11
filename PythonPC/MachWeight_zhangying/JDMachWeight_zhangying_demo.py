import warnings
from queue import Queue
from tkinter.filedialog import askopenfilename
import pandas as pd  # 先装个pandas ,pip install pandas
from tkinter import *
from tkinter import messagebox
import requests

import pymysql as pymysql
import time
import tkinter as tk

from PythonPC.MachWeight_tixiang.forExcel import write_excel

def intoExcel():

    path = e2.get()

    # 建立数据库连接
    db = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                         db='JDWL')
    cursor = db.cursor()

    try:
        data = pd.read_excel(path)
    except:
        tk.messagebox.showinfo(title="路径出错", message="请检查导入路径")
        return
    name = var.get()
    # 判断数据表是否存在
    if var.get() == "张英":
        try:
            cursor.execute(
                'CREATE TABLE OrderWeight_%s  (`tknum` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`order_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`weight` double(5, 2) NOT NULL,`ischeck` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT "0",`order_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",`set_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",PRIMARY KEY (`tknum`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;'%name)
        except:
            print('已存在的表')
        query = 'insert ignore into OrderWeight_%s (tknum,order_per,weight ,order_time) values (%s,%s,%s,%s)'%name
    elif var.get() == "橘子君":
        try:
            cursor.execute(
                'CREATE TABLE `OrderWeight_juzijun`  (`tknum` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`order_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`weight` double(5, 2) NOT NULL,`ischeck` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT "0",`order_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",`set_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",PRIMARY KEY (`tknum`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;')
        except:
            print('已存在的表')
        query = 'insert ignore into OrderWeight_juzijun(tknum,order_per,weight ,order_time) values (%s,%s,%s,%s)'
    elif var.get() == "提象":
        try:
            cursor.execute(
                'CREATE TABLE `OrderWeight_tixiang`  (`tknum` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`order_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`send_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`receive_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`weight` double(5, 2) NOT NULL,`ischeck` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT "0",`order_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",`set_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",PRIMARY KEY (`tknum`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;')
        except:
            print('已存在的表')
        try:
            cursor.execute(
                'CREATE TABLE `CheckWeight_tixiang`  (`tknum` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`order_per` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`order_weight` double(5, 2) NOT NULL,`real_weight` double(5, 2) NOT NULL,`over_weight` double(5, 2) NULL DEFAULT NULL,`status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`order_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "下单时间",`check_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",`send_per` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`receive_per` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,PRIMARY KEY (`tknum`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;')
        except:
            print('已存在的表')
        query = 'insert ignore into OrderWeight_tixiang(tknum,order_per,weight ,order_time ,send_per, receive_per) values (%s,%s,%s,%s,%s,%s)'
    else:
        tk.messagebox.showinfo(title="账号出错", message="请选择核重账号")
        return


    for i in range(1, len(data)):
        tknum = data.iloc[i, 1]
        order_per = data.iloc[i, 10]
        weight = data.iloc[i, 32]
        order_time = data.iloc[i, 23]
        send_per = data.iloc[i, 13]
        receive_per = data.iloc[i, 17]

        try:
            values = (str(tknum), str(order_per), float(weight), str(order_time), str(send_per), str(receive_per))
            cursor.execute(query, values)
        except:
            tk.messagebox.showinfo(title="数据出错", message="请检查导入表格 或 联系管理员")
            return
        print("已经处理"+ str(i) +"条数据")
    db.commit()
    tk.messagebox.showinfo(title="导入完成", message="导入成功")

    cursor.close()
    db.close()

def run():

    client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
    cursor = client.cursor()

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
        sql_selectnumbers = 'select tknum from OrderWeight_juzijun where ischeck = "0" and order_per = "jd_EyrEhvU"'
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
    elif var.get() == "提象":
        sql_setcheckweight = 'insert ignore into CheckWeight_tixiang (tknum,order_weight,real_weight,over_weight,status,order_time, order_per, send_per, receive_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        sql_selectnumbers = 'select tknum from OrderWeight_tixiang where ischeck = "0" and order_per = "徐-提像"'
        sql_selectweight = 'select weight from OrderWeight_tixiang where tknum = %s'
        sql_01 = 'select send_per from OrderWeight_tixiang where tknum = %s'
        sql_02 = 'select receive_per from OrderWeight_tixiang where tknum = %s'
        sql_updatechaozhong = 'update OrderWeight_tixiang set ischeck = "超重" where tknum = %s'
        sql_shaozhong = 'update OrderWeight_tixiang set ischeck = "少重" where tknum = %s'
        sql_zhengchang = 'update OrderWeight_tixiang set ischeck = "正常" where tknum = %s'
        sql_zhongzholanshou = 'update OrderWeight_tixiang set ischeck = "终止揽收" where tknum = %s'
        sql_kehuquxiao = 'update OrderWeight_tixiang set ischeck = "客户取消" where tknum = %s'
        sql_wudanhao = 'update OrderWeight_tixiang set ischeck = "无单号" where tknum = %s'
        sql_selectordertime = 'select order_time from OrderWeight_tixiang where tknum = %s'
        sql_realweight = 'select * from CheckWeight_tixiang where check_time like %s'
        sql_selectorderper = 'select order_per from OrderWeight_tixiang where tknum = %s'

    else:
        tk.messagebox.showinfo(title="账号出错", message="请选择核重账号")
        return



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
            try:

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

                    cursor.execute(sql_01, [tknum])
                    send_per = cursor.fetchall()

                    cursor.execute(sql_02, [tknum])
                    receive_per = cursor.fetchall()

                    if chazhi > 0:
                        cursor.execute(sql_setcheckweight, [tknum, ow, rw, chazhi, s, order_time, order_per, send_per, receive_per])
                        cursor.execute(sql_updatechaozhong, [tknum])
                        print("已经检查到第" + str(num) + "条为超重，单号为：" + tknum[0])
                        num += 1
                    elif chazhi < -1:
                        cursor.execute(sql_setcheckweight, [tknum, ow, rw, chazhi, s, order_time, order_per, send_per, receive_per])
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
            except:
                tk.messagebox.showinfo(title="核重出错", message="请检查cookie是否有误 或 联系管理员")
                return

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
    tk.messagebox.showinfo(title="核重完成", message="核重成功")

# warnings.filterwarnings("ignore")

window = tk.Tk()
window.title("核重")
window.geometry("500x450")

l = tk.Label(window, bg='yellow', width=20, text='请选择需要核重的账号')
l.place(x=190, y=20)


def print_selection():
    l.config(text='核重账号:' + var.get())

var = tk.StringVar()
var.set(0)

r1 = tk.Radiobutton(window, text='张英', variable=var, value='张英', command=print_selection)
r1.place(x=200, y=50)
r2 = tk.Radiobutton(window, text='橘子君', variable=var, value='橘子君', command=print_selection)
r2.place(x=200, y=70)
r3 = tk.Radiobutton(window, text='提象', variable=var, value='提象', command=print_selection)
r3.place(x=200, y=90)


def selectPath():
    path_ = askopenfilename()
    path.set(path_)

path = StringVar()

Label(window, text="目标路径:").place(x=50, y=150)
e2 = tk.Entry(window, textvariable=path, width=29)
e2.place(x=135, y=150)

Button(window, text="路径选择", command=selectPath).place(x=350, y=150)
b = tk.Button(window, text='导入数据', width=15, height=2, command=intoExcel)
b.place(x=200, y=200)

tk.Label(window, text='请输入cookie值:').place(x=20, y=300)
e = tk.Entry(window, width=38)
e.place(x=130, y=300)


b = tk.Button(window, text='开始核重', width=15, height=2, command=run)
b.place(x=200, y=360)

window.mainloop()