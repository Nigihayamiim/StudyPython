import telnetlib

import requests
from fake_useragent import UserAgent

url = "https://httpbin.org/ip"

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080"
}

headers = {
    "User-Agent": UserAgent().chrome
}

response = requests.get(url, proxies=proxies, headers=headers)
print(response.text)

