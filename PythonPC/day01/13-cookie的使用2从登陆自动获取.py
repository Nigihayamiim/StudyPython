from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPHandler
from urllib.parse import urlencode
from fake_useragent import UserAgent

login_url = "https://user.darentui.com/v1/user/login/"
headers = {
    "User-Agent": UserAgent().chrome
}
form_data = {
    "cellphone": "18523870797",
    "password": "x12301230"
}
data = urlencode(form_data)
request1 = Request(login_url, data=data.encode(), headers=headers)
handler1 = HTTPHandler({"http":"182.138.160.189:8118"})
opener1 = build_opener(handler1)
response1 = opener1.open(request1)
print(response1.read().decode())

info_url = "https://digital.darentui.com/api/v1/rank/live_streaming_rank/?page=1&date=2020-04-27"
request2 = Request(info_url, headers=headers)
handler2 = HTTPCookieProcessor()
opener2 = build_opener(handler1, handler2)
response2 = opener2.open(request2)
print(response2.read().decode())

