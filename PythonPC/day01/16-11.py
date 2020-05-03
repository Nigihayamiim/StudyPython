import telnetlib

import requests
from fake_useragent import UserAgent

url = "https://httpbin.org/ip"

proxies = {
    "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
    "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
}

headers = {
    "User-Agent": UserAgent().chrome
}

response = requests.get(url, proxies=proxies, headers=headers)
print(response.text)

