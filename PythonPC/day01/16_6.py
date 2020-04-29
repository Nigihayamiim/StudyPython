import requests
from fake_useragent import UserAgent

url = "https://tieba.baidu.com/f?ie=utf-8&{}"
headers = {
    "User-Agent": UserAgent().chrome
}
content = input("请输入要下载的内容:")
num = input("请输入要下载的页数:")
for pn in range(int(num)):
    params = {
        "kw": content,
        "pn": pn * 50
    }
    filename = content + "吧第" + str(pn+1) + "页的内容.txt"
    print("正在下载" + filename)
    response = requests.get(url, headers=headers, params=params)
    with open(filename, "wb") as f:
        f.write(response.text.encode())
