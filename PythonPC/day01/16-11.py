import telnetlib

import requests
from fake_useragent import UserAgent

url = "https://httpbin.org/ip"

proxies = {
    "http": "http://fqcs1:fqcs1@106.4.212.228:65000",
    "https": "http://fqcs1:fqcs1@106.4.212.228:65000"
}

headers = {
    "User-Agent": UserAgent().chrome
}

response = requests.get(url, proxies=proxies, headers=headers)
print(response.text)

