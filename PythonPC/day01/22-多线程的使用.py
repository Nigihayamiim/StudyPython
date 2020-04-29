from threading import Thread
from queue import Queue
from fake_useragent import UserAgent
import requests
from lxml import etree


class CrawlInfo(Thread):
    # 爬虫类
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        while not self.url_queue.empty():
            response = requests.get(self.url_queue.get(), headers=headers)
            #print(response.text)
            if response.status_code == 200:
                self.html_queue.put(response.text)

class ParseInfo(Thread):
    # 解析类
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        with open("笑话2.txt", "w", encoding="utf-8") as f:
            while not self.html_queue.empty():
                e = etree.HTML(self.html_queue.get())
                span_contents = e.xpath("//div[@class='content']/span[1]")
                for span in span_contents:
                    info = span.xpath('string(.)')
                    f.write(info)

if __name__ == '__main__':
    base_url = "https://www.qiushibaike.com/text/page/{}"
    # 存储url的容器
    url_queue = Queue()
    # 存储内容的容器
    html_queue = Queue()
    for i in range(1,14):
        new_url = base_url.format(i)
        url_queue.put(new_url)
    # 创建爬虫
    crawl_list = []
    for i in range(0, 3):
        crawl = CrawlInfo(url_queue, html_queue)
        crawl_list.append(crawl)
        crawl.start()
    for crawl in crawl_list:
        crawl.join()

    # 创建解析
    parse_list = []
    for i in range(0, 3):
        parse = CrawlInfo(url_queue, html_queue)
        parse_list.append(parse)
        parse.start()
    for parse in parse_list:
        parse.join()

    # crawl = CrawlInfo(url_queue, html_queue)
    # crawl.start()
    # crawl.join()
    # parse = CrawlInfo(url_queue, html_queue)
    # parse.start()
    # parse.join()