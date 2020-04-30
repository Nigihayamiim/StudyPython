import requests
from fake_useragent import UserAgent

login_url = "https://api-service.chanmama.com/v1/access/token"
session = requests.Session()
headers = {
    "User-Agent": UserAgent().chrome
}
form_data = {
    "username": "18523870797",
    "password": "x12301230"
}
proxies = {
    "http": "http://117.88.176.145:3000"
}

response = session.post(login_url, data=form_data, headers=headers, proxies=proxies)
info = response.text
print(response.text)

info_url = "https://toobigdata.com/douyin/promotions?page=3"
response2 = session.get(info_url, headers=headers, proxies=proxies)
print(response2.text)

