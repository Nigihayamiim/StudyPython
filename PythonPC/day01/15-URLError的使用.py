from urllib.error import URLError
from urllib.request import Request, urlopen
from fake_useragent import UserAgent

url = "https://digital.darentui.com/s"
headers = {
    "User-Agent": UserAgent().chrome
}
try:
    req = Request(url, headers=headers)
    resp = urlopen(req)
    print(resp.read().decode())
except URLError as e :
    if not e.args:
        print(e.code)
    elif e.args[0].errno == 11001:
        print(e.args[0].errno)