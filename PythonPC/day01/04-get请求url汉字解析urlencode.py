from urllib.request import Request,urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent

args = {
    "wd": "贴吧",
    "ie": "utf-8"
}
url = "https://www.baidu.com/s?{}".format(urlencode(args))
print(url)
headers = {
    "User-Agent": UserAgent().random
}
request = Request(url, headers=headers)
print(request.get_header("User-agent"))
response = urlopen(request)
print(response.read().decode())