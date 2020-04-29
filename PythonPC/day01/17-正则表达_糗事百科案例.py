import re

from fake_useragent import UserAgent
import requests

url = "https://www.qiushibaike.com/text/"

headers = {
    "User-Agent": UserAgent().random
}
proxies = {
    "http": "http://http://117.88.4.91:3000"
}
response = requests.get(url, headers=headers, proxies=proxies)
info = response.text
infos = re.findall(r'<div class="content">\s*<span>\s*(.+)\s*</span>', info)
with open("笑话.txt","a", encoding="utf-8") as f:
    for i in infos:
        f.write(i + "\n\n")