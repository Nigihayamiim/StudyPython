from urllib.request import Request, urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent

url = "https://user.darentui.com/v1/user/login/"
form_data = {
    "cellphone": "18523870797",
    "password": "x12301230"
}
f_data = urlencode(form_data)
headers = {
    "User-Agent": UserAgent().chrome
}
request = Request(url, data=f_data.encode(), headers=headers)
response = urlopen(request)
print(response.read().decode())