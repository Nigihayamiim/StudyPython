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
url = "https://youcloud.com/login/appgrowing/"

shop_url_queue = Queue()

client = pymysql.connect(host='49.233.3.208', port=3306, user='root', password='x1113822624', charset='utf8',
                             db='forTel')
cursor = client.cursor()
sql_goods = 'insert ignore into goods values (%s, %s, %s)'
sql_shop = 'insert ignore into shop(shop_name,shop_tel,shop_position,bus_name,goods_num,sales_up) values (%s,%s,%s,%s,%s,%s)'
sql_shop_name = 'insert ignore into shop_name values (%s)'

warnings.filterwarnings("ignore")


# 进入浏览器设置
options = webdriver.ChromeOptions()
# 谷歌无头模式
# options.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--disable-gpu')
# 更换头部
options.add_argument('user-agent=' + 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36')

driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

driver.find_element_by_xpath('//input[@name="account"]').send_keys('13157128103')
sleep(randint(1, 2))

driver.find_element_by_xpath('//input[@name="password"]').send_keys('1234567890')
sleep(randint(1, 2))

driver.find_element_by_xpath('//button[@data-lang="login"]').click()
sleep(randint(2, 3))

driver.find_element_by_xpath('//*[@id="app"]/header/nav/div/ul/li[4]/a').click()
sleep(randint(2, 3))

driver.find_element_by_xpath('//li[10]/a/span[2]').click()
sleep(randint(2, 3))

driver.find_element_by_xpath('//div[2]/div[3]//div/input').click()
sleep(randint(1, 2))

driver.find_element_by_xpath('//div[1]/div[1]/ul/li[7]').click()
sleep(randint(2, 3))

# element = driver.find_element_by_xpath('//input[@type="number"]')
# element.send_keys(Keys.CONTROL, 'a')
# element.send_keys('556')
# driver.find_element_by_xpath('//button[@class="btn-next"]').click()
# sleep(5)


page = 1
num = 1

name_signs = "//div[2]//tr[{}]/td[3]//a"
# bus_signs = "//div[3]//tr[{}]/td[4]//a"
goods_signs = '//div[3]//tr[{}]/td[5]/div/a'
up_signs = '//div[3]//tr[{}]/td[6]/div/span'

while True:
    print("这是第" + str(page) + "页的内容")

    for i in range(1, 21):
        name_sign = name_signs.format(i)
        shop_name = driver.find_element_by_xpath(name_sign).text
        goods_num = driver.find_element_by_xpath(goods_signs.format(i)).text
        sales_up = driver.find_element_by_xpath(up_signs.format(i)).text
        result = cursor.execute(sql_shop_name, [shop_name])

        if result:
            base_sign = name_signs.format(i)
            try:
                element = driver.find_element_by_xpath(base_sign)
                driver.execute_script("arguments[0].click();", element)
            except Exception:
                print("第"+str(num)+"条数据出现超时,尝试再次连接")
                element = driver.find_element_by_xpath(base_sign)
                driver.execute_script("arguments[0].click();", element)
            sleep(1)

            all_hand = driver.window_handles
            driver.switch_to.window(all_hand[-1])

            html = driver.page_source

            shop_name = driver.find_element_by_xpath('//div[1]/div[1]/span[@class="title"]').text
            shop_tel = ','.join(re.findall(r'class="el-dropdown-menu__item agc-shop-base__dropdown-item">(.*?)</li>', html))
            if not shop_tel:
                shop_tel = driver.find_element_by_xpath('//div[1]/div[2]/div[1]/div[2]/span').text
            shop_address = driver.find_element_by_xpath('//div[3]/div[2]/span').text
            bus_name = driver.find_element_by_xpath('//div[2]/div[2]/div[2]/span').text


            result = cursor.execute(sql_shop, [shop_name, shop_tel, shop_address, bus_name, goods_num, sales_up])

            if result:
                print("成功添加了" + str(num) + "条数据")
                num += 1
                client.commit()

            driver.close()
            driver.switch_to.window(all_hand[0])

    print("第" + str(page) + "页的内容搜集完毕")

    # if goods_salas < 5:
    #     print("日销量5以下，不找啦")
    #     break

    driver.find_element_by_xpath('//button[@class="btn-next"]').click()
    page += 1
    sleep(randint(3, 5))
