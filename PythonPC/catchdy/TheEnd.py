# url管理
class URLManager:
    # 初始化
    def __init__(self):
        self.goods_url = []
        self.shops_url = []
    # 获取一个url
    def get_good_url(self):
        good_url = self.goods_url.pop()
        return good_url

    def get_shop_url(self):
        shop_url = self.shops_url.pop()
        return shop_url
# 爬取

# 数据解析

# 数据处理

# 调度