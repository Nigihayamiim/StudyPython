import pymysql as pymysql

from PythonPC.IntoExcel.forExcel import write_excel

date = "2020-07-19%"
filename = date + "新2全国超重少重统计.xls"


conn = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='JDWL')
cursor = conn.cursor()
sql_realweight = 'select * from CheckWeight_new2 where check_time like %s'
cursor.execute(sql_realweight, [date])
datas = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()

write_excel(datas, filename, date)