import pymysql

client = pymysql.connect(host='106.53.192.189', port=3306, user='root', password='x1113822624', db='shop',charset='utf8')
cursor = client.cursor()
sql_shop = 'insert ignore into shop(shop_id,shop_name,shop_tel,shop_position) values ("abCsjUW","茜茜服饰商行","15779119280","广东省")'
result = cursor.execute(sql_shop)
if result:
    print("添加成功")
else:
    print("添加失败")
print(result)