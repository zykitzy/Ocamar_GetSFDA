import scrapy


class SFDAItem(scrapy.Item):
    xu_hao = scrapy.Field()  # 序号
    yao_pin_name = scrapy.Field()  # 药品名称
    pi_zhun_num = scrapy.Field()  # 批准文号，主要对象
    sheng_chan_company = scrapy.Field()  # 生产厂商
    zhi_ji = scrapy.Field()  # 制剂
    gui_ge = scrapy.Field()  # 规格

    def __init__(self, name):
        self.name = name

    def __setitem__(self, k, v):
        self.k = v

    def __str__(self):
        return "name:%s, %s" % (self.name, self.k)