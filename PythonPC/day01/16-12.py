import requests
from fake_useragent import UserAgent

login_url = "https://digital.darentui.com/#/login"
session = requests.Session()
headers = {
    "User-Agent": UserAgent().chrome
}

form_data = {
    "cellphone": "18523870797",
    "password": "x12301230"
}

proxies = {
    "http": "http://117.88.4.91:3000"
}

response = session.get(login_url, proxies=proxies, headers=headers, data=form_data)
print(response.text)
info_url = "https://digital.darentui.com/api/v1/rank/live_streaming_rank/?page=1&date=2020-04-27"
resp = session.get(info_url, proxies=proxies, headers=headers)
print(resp.text)