import requests
from fake_useragent import UserAgent
from urllib3.exceptions import NewConnectionError

url = "https://httpbin.org/ip"

proxies = {
    "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
    "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
}

headers = {
    "User-Agent": UserAgent().chrome
}

try:
    response = requests.get(url, proxies=proxies, headers=headers)
    print(response.text)
except Exception as e:
    print("连接超时,尝试再次连接")
    response = requests.get(url, proxies=proxies, headers=headers)
print("继续运行")

