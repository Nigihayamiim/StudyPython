import re

from jsonpath import jsonpath
import requests
from fake_useragent import UserAgent

url = "https://api-service.chanmama.com/v1/product/search"

headers = {
    "Connection": "keep-alive",
    "Content-Length": "242",
    "Host": "api-service.chanmama.com",
    "Origin": "https://www.chanmama.com",
    "Referer": "https://www.chanmama.com/promotionRank?cat=&keyword=",
    "User-Agent": UserAgent().chrome,
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNTg5MjIzNjAwLCJpYXQiOjE1ODg2Njc1NzUsImlkIjoxMTM3MjZ9.4hew7o-Hf-q8xDLX2xSvRIcHbUcQhBXqJQQlQdCQXPk"
}
proxies = {
    "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
    "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
}

request_payload = {
    "keyword": "", "keyword_type": "", "page": 1, "price": "", "size": 50, "filter_coupon": 0, "is_aweme_goods": 0,
    "tb_max_commission_rate": "", "day_pv_count": "", "day_order_count": "", "cat": "", "platform": "jinritemai",
    "sort": "day_pv_count", "order_by": "desc"
}

response = requests.post(url, headers=headers, proxies=proxies, data=request_payload)
info = response.json()
promotion_id = jsonpath(info, '')
print()
