from pyquery import PyQuery
import requests
from fake_useragent import UserAgent

url = "https://www.xicidaili.com/nn/"
headers = {
    "User-Agent": UserAgent().chrome
}
response = requests.get(url, headers=headers)
doc = PyQuery(response.text)
docs = doc('#ip_list tr')
for i in range(1, docs.length):
    ips = docs.eq(i).find('td').eq(1).text()
    ports = docs.eq(i).find('td').eq(2).text()
    types = docs.eq(i).find('td').eq(5).text()
    print(ips, ":", ports, "\t", types)
