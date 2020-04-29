import requests
from fake_useragent import UserAgent

headers = {
    "User-Agent": UserAgent().chrome
}
url = "https://www.baidu.com/s?"
params = {
    "wd": "贴吧"
}
response = requests.get(url, params=params, headers=headers)
print(response.text)