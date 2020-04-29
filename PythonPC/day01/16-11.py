import requests
from fake_useragent import UserAgent

url = "http://httpbin.org/get"

proxies = {
    "http": "http://117.88.4.91:3000"
}

headers = {
    "User-Agent": UserAgent().chrome
}

response = requests.get(url, proxies=proxies, headers=headers)
print(response.text)