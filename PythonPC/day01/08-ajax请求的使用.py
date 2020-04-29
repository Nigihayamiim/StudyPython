from urllib.request import Request, urlopen
from fake_useragent import UserAgent

bese_url = "https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start={}&limit=20"
num = 0
while True:
    headers = {
        "User-Agent": UserAgent().chrome
    }
    url = bese_url.format(num*20)
    request = Request(url, headers=headers)
    response = urlopen(request)
    info = response.read().decode()
    if not info:
        break
    print(info)
    num += 1
