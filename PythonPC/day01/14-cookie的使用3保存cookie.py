from http.cookiejar import MozillaCookieJar
from urllib.request import Request, build_opener, urlopen, HTTPCookieProcessor
from urllib.parse import urlencode
from fake_useragent import UserAgent

def get_cookie():
    url = "https://user.darentui.com/v1/user/login/"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    form_data = {
        "cellphone": "18523870797",
        "password": "x12301230"
    }
    f_data = urlencode(form_data)
    request = Request(url, data=f_data.encode(), headers=headers)
    cookie_jar = MozillaCookieJar()
    handler = HTTPCookieProcessor(cookie_jar)
    opener = build_opener(handler)
    response = opener.open(request)
    cookie_jar.save("cookie.txt", ignore_discard=True, ignore_expires=True)
    print(response.read().decode())

def use_cookie():
    url = "https://digital.darentui.com/api/v1/rank/dy_sales_rank/?page=1&date=2020-04-27"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    request = Request(url, headers=headers)
    cookie_jar = MozillaCookieJar()
    cookie_jar.load("cookie.txt", ignore_discard=True, ignore_expires=True)
    handler = HTTPCookieProcessor(cookie_jar)
    opener = build_opener(handler)
    response = opener.open(request)
    print(response.read().decode())

if __name__ == '__main__':
    get_cookie()
    use_cookie()