import pymysql as pymysql

from PythonPC.catchdy.forEccel_luban import write_excel

date = "2020-06-26%"
filename = date + "抖音鲁班商家信息.xls"


conn = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='forTel')
cursor = conn.cursor()
sql_shopTel = 'select * from shop where set_date like %s and shop_tel regexp "^1[0-9]{10}$"'
cursor.execute(sql_shopTel, [date])
datas = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()

write_excel(datas, filename, date)