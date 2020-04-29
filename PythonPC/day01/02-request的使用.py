from urllib.request import urlopen
from urllib.request import Request
from fake_useragent import UserAgent

url = "https://www.chanmama.com"
ua = UserAgent()
print(ua.chrome)
headers = {
    "User-Agent": ua.chrome
}

request = Request(url, headers=headers)
print(request.get_header('User-agent'))
response = urlopen(request)

info = response.read()

