import json

import requests
from fake_useragent import UserAgent

url = "https://api-service.chanmama.com/v1/product/search"

payloadData = {
    "page": 1,
    "platform": "jinritemai",
    "size": 200
}

headers = {
    "User-Agent": UserAgent().chrome,
    "Content-Type": "application/json;charset=UTF-8",
    "Host": "api-service.chanmama.com"
}

proxies = {
    "http": "http://117.88.176.145:3000"
}

response = requests.get(url, data=json.dumps(payloadData), headers=headers)
info = response.text
print(info)