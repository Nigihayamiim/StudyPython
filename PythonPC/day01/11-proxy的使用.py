from urllib.request import Request, build_opener, ProxyHandler
from fake_useragent import UserAgent

url = "http://httpbin.org/get"
headers = {
    "User-Agent": UserAgent().chrome
}
request = Request(url, headers=headers)
# 格式(没用户名和密码则不写)
# handler = ProxyHandler({"http(https)": "username:password@ip:port(端口)"})
handler = ProxyHandler({"http": "117.88.176.145:3000"})
opener = build_opener(handler)
response = opener.open(request)
print(response.read().decode())