# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml import etree
from scrapy.http import Request
from time import sleep
from Ocamar_GetSFDA.Items import SFDA_Item
from Ocamar_GetSFDA.Helper.Logger import Logger


# 爬虫主类
class SFDASpider(scrapy.Spider):
    search_cx = "葡萄糖"
    search_name = "葡萄糖注射液"
    count = 1
    name = "SFDASpider"  # 这个程序要执行的唯一标识名  可以自己设置
    start_urls = ["http://app2.sfda.gov.cn/datasearchp"
                  "/all.do"
                  "?page=1"  # 翻页参数
                  "&name={1}"  # 查询详细名称
                  "&tableName=TABLE25&formRender=cx"
                  "&searchcx={0}".format(search_cx, search_name)]  # 首页网址
    url = "http://app2.sfda.gov.cn/datasearchp/" \
          "all.do?name={1}" \
          "&tableName=TABLE25" \
          "&formRender=cx" \
          "&searchcx={0}" \
        .format(search_cx, search_name)
    logger = Logger.logger
    data = []

    def parse(self, response):  # 默认函数parse
        self.count += 1
        driver = webdriver.Edge()
        print(response.url)
        driver.get(response.url)
        sleep(0.5)  # 等待，防止未解析
        body = etree.HTML(driver.page_source)
        self.logger.info(driver.page_source)
        driver.close()

        tr_list = body.xpath('//table[@class="msgtab"]/tbody/tr')
        for tr in tr_list:
            td_list = tr.xpath("./td")
            if len(td_list) > 0:
                item = SFDA_Item
                item.xu_hao = td_list[0].text
                item.yao_pin_name = td_list[1].xpath("./a")[0].text
                item.pi_zhun_num = td_list[2].text
                item.sheng_chan_company = td_list[3].xpath("./a")[0].text
                item.zhi_ji = td_list[4].text
                item.gui_ge = td_list[5].text
                self.data.append(item)

        new_url = self.url + "&page={0}".format(self.count)
        sleep(0.5)

        yield Request(url=new_url, callback=self.parse_detail)

    def parse_detail(self, response):
        for item in self.data:
            print(item.xu_hao)
            print(item.yao_pin_name)
            print(item.pi_zhun_num)
            print(item.sheng_chan_company)
            print(item.gui_ge)
            print(item.zhi_ji)

        if self.count <= 2:
            return self.parse(response)
        else:
            return None


