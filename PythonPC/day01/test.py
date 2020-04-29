import re

import requests
from fake_useragent import UserAgent

url = "https://toobigdata.com/douyin/promotions/"
headers = {
    "User-Agent": UserAgent().chrome,
    "Cookie": "_ga=GA1.2.1891294568.1587479976; __gads=ID=196a438dbf4084b2:T=1587480069:S=ALNI_MY-q1HznH1BF4_h56rL3jj0auybag; _gid=GA1.2.1902672060.1587958221; Hm_lvt_09720a8dd79381f0fd2793fad156ddfa=1587805125,1587958221,1588039492,1588044735; _gat_gtag_UA_8981755_3=1; Hm_cv_09720a8dd79381f0fd2793fad156ddfa=1*email*guest!*!*!1*role*guest; XSRF-TOKEN=eyJpdiI6ImVNSGZtU3Q1cjAyakNuTzhzbmlvY0E9PSIsInZhbHVlIjoiVmdmQVhiaUhPUDNiR0d3aUVNVHlmbUhJVWZ1WEN4ZW1DUXJXQm0yZEszRTJHa0RXalkyM3l4V2dETTdrZ3NxcSIsIm1hYyI6IjMwMTVlOTkzOWFkN2YyZTBiYTRhMzA5NDY3Y2I5NzMyNGUwODczYjA0MTc4NTc3MzZjNDZmM2I0OTA2NTczN2UifQ%3D%3D; toobigdata_session=eyJpdiI6IjY2NjMrcWY4cjRYcGhZZVc0ZFhkR2c9PSIsInZhbHVlIjoiYXdMS01QcmJPTTdLd2FCcUJlZnI1UFBsZlJwR1hMK2tidElGMVJWWTdJUVVvVFlUUGVzNUhGXC9vRTNUTkRxaTIiLCJtYWMiOiJjNWI0NGM2NTIyMTBkZGNiNjdkMWZkNWFiZjllOGZiMWUwNTg2MzlhNjYwYjRhMDc1YWIzMDU4OTgyM2UwZWIzIn0%3D; Hm_lpvt_09720a8dd79381f0fd2793fad156ddfa=1588044753"
}

proxies = {
    "http": "http://117.88.4.91:3000"
}

response = requests.get(url, proxies=proxies, headers=headers)
response.encoding = "utf-8"
info = response.text
# print(info)
infos = re.findall(r'<a href="/douyin/promotion/g/(3.*)" target="_blank">', info)

base_shop_url = "https://ec.snssdk.com/product/fxgajaxstaticitem?id={}&b_type_new=0&device_id=0"
for sjid in infos:
    shop_url = base_shop_url.format(sjid)
    response = requests.get(shop_url, proxies=proxies, headers=headers)
    response.encoding = "utf-8"
    shop = response.text
    shop_name = re.findall(r'"shop_name":"()"', shop)
    shop_tel = re.findall(r'"shop_tel":"()"', shop)