from time import sleep

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.huya.com/g/seeTogether")
page = 1
while True:
    print("-------------这是第" + str(page) + "页的内容-----------")
    sleep(3)
    names = driver.find_elements_by_xpath('//i[@class="nick"]')
    counts = driver.find_elements_by_xpath('//i[@class="js-num"]')
    for name, count in zip(names, counts):
        print(name.text + " : " + count.text)
    page += 1
    if driver.page_source.find('laypage_next') != -1:
        driver.find_element_by_xpath('//a[@class="laypage_next"]').click()
    else:
        break
