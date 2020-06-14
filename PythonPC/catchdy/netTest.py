import requests

url = "https://httpbin.org/get"

proxies = {
            "http": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000",
            "https": "http://0502fq1t1m:0502fq1t1m@59.55.158.225:65000"
        }

response = requests.get(url, proxies=proxies)
print("成功"+response.text)
