from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import ssl

url = "https://www.12306.cn/index/"
headers = {
    "User-Agent": UserAgent().chrome
}
request = Request(url, headers=headers)
# 引用ssl 创建忽略证书对象
comtext = ssl._create_unverified_context()
response = urlopen(request, comtext=comtext)
info = response.read().decode()
print(info)