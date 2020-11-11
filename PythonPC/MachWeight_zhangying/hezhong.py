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
    if name == "":
        tk.messagebox.showinfo(title="账号出错", message="请输入核重账号下单人名称")
        return
    else:
        try:
            cursor.execute(
                'CREATE TABLE `OrderWeight_%s`'%name + '  (`tknum` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`order_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`send_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`receive_per` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`weight` double(5, 2) NOT NULL,`ischeck` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT "0",`order_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",`set_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",PRIMARY KEY (`tknum`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;')
        except:
            print('已存在的表')
        try:
            cursor.execute(
                'CREATE TABLE `CheckWeight_%s`'%name + '  (`tknum` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`order_per` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`order_weight` double(5, 2) NOT NULL,`real_weight` double(5, 2) NOT NULL,`over_weight` double(5, 2) NULL DEFAULT NULL,`status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`order_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "下单时间",`check_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT "创建时间",`send_per` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`receive_per` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,PRIMARY KEY (`tknum`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;')
        except:
            print('已存在的表')
        query = 'insert ignore into `OrderWeight_%s`'%name + '(tknum,order_per,weight ,order_time ,send_per, receive_per) values (%s,%s,%s,%s,%s,%s)'

    list = data.columns.values

    for i in range(1, len(data)):
        for j in range(len(list)):
            if list[j] == '运单号':
                tknum = data.iloc[i, j]
            elif list[j] == '下单人':
                order_per = data.iloc[i, j]
            elif list[j] == '下单重量(kg)':
                weight = data.iloc[i, j]
            elif list[j] == '下单时间':
                order_time = data.iloc[i, j]
            elif list[j] == '寄件人':
                send_per = data.iloc[i, j]
            elif list[j] == '收件人':
                receive_per = data.iloc[i, j]

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
    name = var.get()
    if name == "":
        tk.messagebox.showinfo(title="账号出错", message="请输入核重账号下单人名称")
        return
    else:
        sql_setcheckweight = 'insert ignore into `CheckWeight_%s`'%name + ' (tknum,order_weight,real_weight,over_weight,status,order_time, order_per, send_per, receive_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        sql_selectnumbers = 'select tknum from `OrderWeight_%s`'%name +' where ischeck = "0" and order_per = "%s"'%name
        sql_selectweight = 'select weight from `OrderWeight_%s`'%name +' where tknum = %s'
        sql_01 = 'select send_per from `OrderWeight_%s`'%name +' where tknum = %s'
        sql_02 = 'select receive_per from `OrderWeight_%s`'%name +' where tknum = %s'
        sql_updatechaozhong = 'update `OrderWeight_%s`'%name +' set ischeck = "超重" where tknum = %s'
        sql_shaozhong = 'update `OrderWeight_%s`'%name +' set ischeck = "少重" where tknum = %s'
        sql_zhengchang = 'update `OrderWeight_%s`'%name +' set ischeck = "正常" where tknum = %s'
        sql_zhongzholanshou = 'update `OrderWeight_%s`'%name +' set ischeck = "终止揽收" where tknum = %s'
        sql_kehuquxiao = 'update `OrderWeight_%s`'%name +' set ischeck = "客户取消" where tknum = %s'
        sql_wudanhao = 'update `OrderWeight_%s`'%name +' set ischeck = "无单号" where tknum = %s'
        sql_selectordertime = 'select order_time from `OrderWeight_%s`'%name +' where tknum = %s'
        sql_realweight = 'select * from `CheckWeight_%s`'%name +' where check_time like %s'
        sql_selectorderper = 'select order_per from `OrderWeight_%s`'%name +' where tknum = %s'


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
    filename = date + name + "全国超重少重统计.xls"

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
var.set("")

Label(window, text="请输入下单人名称:").place(x=40, y=70)
e2 = tk.Entry(window, textvariable=var, width=20)
e2.place(x=155, y=70)
Button(window, text="确认", command=print_selection).place(x=350, y=70)


# r1 = tk.Radiobutton(window, text='张英', variable=var, value='张英', command=print_selection)
# r1.place(x=200, y=50)
# r2 = tk.Radiobutton(window, text='橘子君', variable=var, value='橘子君', command=print_selection)
# r2.place(x=200, y=70)
# r3 = tk.Radiobutton(window, text='提象', variable=var, value='提象', command=print_selection)
# r3.place(x=200, y=90)


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