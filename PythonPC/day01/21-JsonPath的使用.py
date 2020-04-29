from jsonpath import jsonpath
import requests
import json
from fake_useragent import UserAgent

url = "https://www.lagou.com/lbs/getAllCitySearchLabels.json"

headers = {
    "User-Agent": UserAgent().chrome
}

proxies = {
    "http": "121.237.149.100:3000"
}

response = requests.get(url, proxies=proxies, headers=headers)
names = jsonpath(json.loads(response.text), '$..name')
codes = jsonpath(response.json(), '$..code')

print(names)
print(codes)