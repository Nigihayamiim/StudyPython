import re

import requests
from fake_useragent import UserAgent

url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id=3334052341354747123&b_type_new=0&device_id=0"
headers = {
    "User-Agent": UserAgent().chrome
}
proxies = {
    "http": "111.222.141.127:8118"
}

response = requests.get(url, headers=headers, proxies=proxies)
info = response.text
re.findall(r'"shop_tel":"(1\d+)', info)