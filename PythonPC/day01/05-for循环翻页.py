from urllib.request import Request, urlopen
from fake_useragent import UserAgent
from urllib.parse import quote

content = input("请输入要下载的内容:")
num = input("请输入要下载的页数:")
for pn in range(int(num)):

    url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(quote("魅族"), pn*50)
    print(url)
    headers = {
        "User-Agent": UserAgent().chrome
    }
    request = Request(url, headers=headers)
    response = urlopen(request)
    print(response.read().decode())