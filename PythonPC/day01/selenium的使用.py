from selenium import webdriver

chrome = webdriver.Chrome()

chrome.get("http://baidu.com")
info = chrome.page_source
print(info)
chrome.quit()