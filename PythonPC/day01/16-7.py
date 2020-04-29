import requests
from fake_useragent import UserAgent

url = "https://digital.darentui.com/#/login"
headers = {
    "User-Agent": UserAgent().chrome
}
form_data = {
    "cellphone": "18523870797",
    "password": "x12301230"
}
response = requests.get(url, data=form_data, headers=headers)
print(response.text)