import requests
from fake_useragent import UserAgent

url = "https://www.12306.cn/index/"
headers = {
    "User-Agent": UserAgent().chrome
}
# 关闭警告
requests.packages.urllib3.disable_warnings()
response = requests.get(url, verify=False, headers=headers)
response.encoding = "utf-8"
print(response.text)