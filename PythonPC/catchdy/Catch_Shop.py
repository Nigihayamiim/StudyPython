import re
import warnings
from queue import Queue
from random import randint
from time import sleep

import pymysql
import requests
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys

base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
url = "https://www.boss618.com/"

shop_url_queue = Queue()

client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='forTel')
cursor = client.cursor()
sql_goods = 'insert ignore into goods values (%s, %s, %s)'
sql_shop = 'insert ignore into shop(shop_name,shop_tel,shop_position) values (%s,%s,%s)'
sql_shop_name = 'insert ignore into shop_name values (%s)'

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

driver.find_element_by_xpath('//a[@href="/shop/hot"]/li/span').click()
sleep(randint(5, 6))

driver.find_element_by_xpath('//span[2]//i').click()
sleep(randint(1, 2))

driver.find_element_by_xpath('//div[3]/div[1]/div[1]/ul/li[4]/span').click()
sleep(randint(3, 5))

element = driver.find_element_by_xpath('//input[@type="number"]')
element.send_keys(Keys.CONTROL, 'a')
element.send_keys('556')
driver.find_element_by_xpath('//button[@class="btn-next"]').click()
sleep(5)


page = 556
num = 1
count = 1
while True:
    print("这是第" + str(page) + "页的内容")

    base_signs = "//div[5]//tr[{}]//button[1]"
    name_signs = "//div[4]//tr[{}]/td[2]/div/span"

    for i in range(1, 51):
        name_sign = name_signs.format(i)
        shop_name = driver.find_element_by_xpath(name_sign).text
        result = cursor.execute(sql_shop_name, [shop_name])
        client.commit()
        if result:
            base_sign = base_signs.format(i)
            try:
                driver.find_element_by_xpath(base_sign).click()
            except Exception:
                print("第"+str(count)+"条数据出现超时,尝试再次连接")
                driver.find_element_by_xpath(base_sign).click()
            sleep(1)

            all_hand = driver.window_handles
            driver.switch_to.window(all_hand[-1])

            html = driver.page_source

            shop_name = driver.find_element_by_xpath('//h2').text
            shop_tel = ''.join(re.findall(r'客服电话:(.*?)</p>', html))
            shop_address = ''.join(re.findall(r'联系地址：(.*?)</p>', html))

            result = cursor.execute(sql_shop, [shop_name, shop_tel, shop_address])
            client.commit()
            if result:
                print("成功添加了" + str(num) + "条数据")
                num += 1
            driver.close()
            driver.switch_to.window(all_hand[0])

    print("第" + str(page) + "页的内容搜集完毕")

    # if goods_salas < 5:
    #     print("日销量5以下，不找啦")
    #     break

    driver.find_element_by_xpath('//button[@class="btn-next"]').click()
    page += 1
    sleep(randint(3, 5))
