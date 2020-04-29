import requests
from fake_useragent import UserAgent
from lxml import etree

url = "http://www.farmer.com.cn/2020/04/29/99852237.html"
headers = {
    "User-Agent": UserAgent().chrome
}
response = requests.get(url, headers=headers)
response.encoding = "utf-8"
e = etree.HTML(response.text)

title = e.xpath('//h1/text()')
tag = e.xpath('//div/div[@class="article-meta clearfix"]//span/text()')
re_title = e.xpath('//strong/text()')
content = e.xpath('(//p[@style="text-indent: 2em;"]|//p[@style="text-indent: 2em;"]/span)/text()')
img_urls = e.xpath('//div[@class="article-main"]//img/@src')
print(title)