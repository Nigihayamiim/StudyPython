import re
import warnings
from queue import Queue
from random import randint
from time import sleep

import pymysql
import requests
from selenium import webdriver
from fake_useragent import UserAgent


base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
url = "https://www.boss618.com/"

shop_url_queue = Queue()

client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='forTel')
cursor = client.cursor()
sql_goods = 'insert ignore into goods values (%s, %s, %s)'
sql_shop = 'insert ignore into shop(shop_id,shop_name,shop_tel,shop_position,good_id) values (%s,%s,%s,%s,%s)'
sql_goods_id = 'insert ignore into goods_id values (%s)'

warnings.filterwarnings("ignore")


# 进入浏览器设置
options = webdriver.ChromeOptions()
# 谷歌无头模式
options.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--disable-gpu')
# 更换头部
options.add_argument('user-agent=' + 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36')

driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

driver.find_element_by_xpath('//input[@name="login_name"]').send_keys('17623040397')
sleep(randint(1, 2))

driver.find_element_by_xpath('//input[@name = "password"]').send_keys('x12301230')
sleep(randint(1, 2))

driver.find_element_by_xpath('//button/span').click()
sleep(randint(5, 8))

driver.find_element_by_id('hamburger-container').click()
sleep(randint(1, 2))

driver.find_element_by_xpath('//a[@href="/goods/hot"]/li/span').click()
sleep(randint(6, 10))

# driver.find_element_by_xpath('//div[1]/div/button[2]').click()
# sleep(randint(5, 6))

driver.find_element_by_xpath('//input[@placeholder="开始日期"]').click()
sleep(randint(1, 2))

# driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/button[1]').click()
driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/button[3]').click()
sleep(randint(6, 10))

page = 1
num = 1
count = 1
while True:
    print("这是第" + str(page) + "页的内容")

    html = driver.page_source

    goods_ids = re.findall(r'href="https:\D+(\d{19})"', html)
    goods_Sales = driver.find_element_by_xpath('//div[3]//tr[1]/td[7]/div/span')
    goods_salas = int(goods_Sales.text)

    for goods_id in goods_ids:
        try:
            result = cursor.execute(sql_goods_id, [goods_id])
        except Exception as e:
            client.rollback()
        if result:
            shop_url_queue.put(base_shop_url.format(goods_id))



    headers = {
        "User-Agent": UserAgent().chrome
    }
    proxies = {
        "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
        "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
    }

    while not shop_url_queue.empty():
        shop_url = shop_url_queue.get()
        try:
            response = requests.get(shop_url, headers=headers, proxies=proxies)
        except Exception:
            print("第" + str(count) + "条数据出现超时,尝试再次连接")
            response = requests.get(shop_url, headers=headers, proxies=proxies)
        code = response.status_code
        print("这是第" + str(count) + "条数据,地址为:" + shop_url)
        sleep(randint(0, 1))
        count += 1
        if code == 200:
            response.encoding = "utf-8"
            shop = response.text
            shop_position = ''.join(re.findall(r'"product_province_name":"(.*?)"', shop))
            shop_id = ''.join(re.findall(r'"shop_id":"(.*?)"', shop))
            shop_name = ''.join(re.findall(r'"shop_name":"(.*?)"', shop))
            shop_tel = ''.join(re.findall(r'"shop_tel":"(.*?)"', shop))
            product_id = ''.join(re.findall(r'"product_id":"(.*?)"', shop))
            good_name = ''.join(re.findall(r'"name":"(.*?)"', shop))
            ## result = cursor.execute(sql_goods, [product_id, good_name, shop_id])
            result = cursor.execute(sql_shop, [shop_id, shop_name, shop_tel, shop_position, product_id])
            client.commit()
            if result:
                print("成功添加了" + str(num) + "条数据")
                num += 1
    print("第" + str(page) + "页的内容搜集完毕")

    # if goods_salas < 5:
    #     print("日销量5以下，不找啦")
    #     break

    driver.find_element_by_xpath('//button[@class="btn-next"]').click()
    page += 1
    sleep(randint(6, 12))
