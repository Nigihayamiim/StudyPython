from urllib.request import Request, urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent

def get_html(url):
    headers = {
        "User-Agent": UserAgent().chrome
    }
    request = Request(url, headers=headers)
    response = urlopen(request)
    return response.read()

def save_html(filename, html_bytes):
    with open(filename, "wb") as f:
        f.write(html_bytes)

def main():
    base_url = "https://tieba.baidu.com/f?ie=utf-8&{}"
    content = input("请输入要下载的内容:")
    num = input("请输入要下载的页数:")
    for pn in range(int(num)):
        args = {
            "kw": content,
            "pn": pn*50
        }
        arg = urlencode(args)
        url = base_url.format(arg)
        filename = content + "吧的第" + str(pn+1) + "页.html"
        print(filename + "正在下载")
        html_bytes = get_html(url)
        save_html(filename, html_bytes)

if __name__ == '__main__':
    main()