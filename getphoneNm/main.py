from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Firefox()
driver.get('https://www.chanmama.com/')
sleep(3)
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/div/div[1]/ul/li[2]/div/a').click()
sleep(3)
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div/input').click()
sleep(1)
driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/ul/li[4]').click()