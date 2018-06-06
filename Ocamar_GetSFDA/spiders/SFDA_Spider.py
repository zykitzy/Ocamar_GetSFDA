# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml import etree
from scrapy.http import Request
from time import sleep
from Ocamar_GetSFDA.Items.SFDA_Item import SFDAItem
from Ocamar_GetSFDA.Helper.Logger import Logger
from Ocamar_GetSFDA.Helper.MySqlHelper import Dbsfda
from Ocamar_GetSFDA.Helper.FileHelper import Config
import os

# 爬虫主类
class SFDASpider(scrapy.Spider):

    # 翻页参数
    count = 1
    # 总页数
    total_count = 0
    config_list = Config().get_config()
    # 当前查询的关键字位置
    config_count = 0
    name = "SFDASpider"  # 这个程序要执行的唯一标识名  可以自己设置
    start_urls = ["http://app2.sfda.gov.cn/datasearchp"
                  "/all.do"
                  "?name={0}"  # 查询详细名称
                  "&tableName=TABLE25&formRender=cx"
                  .format(config_list[config_count])]  # 首页网址
    url = "http://app2.sfda.gov.cn/datasearchp/" \
          "all.do?name={0}" \
          "&tableName=TABLE25" \
          "&formRender=cx"
    logger = Logger.logger

    def parse(self, response):  # 默认函数parse
        if len(self.config_list) < 1:
            return   # 配置文件中没有配置查询项，就退出
        # chrome 默认安装位置
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)  # 驱动chrome 来查看网页
        print(response.url)
        driver.get(response.url)
        body = etree.HTML(driver.page_source)
        # self.logger.info(driver.page_source)
        driver.close()  # 关闭浏览器，防止打开过多
        # 解析总页数
        td = body.xpath('//td[contains(text(),"页/共")]')
        if self.total_count == 0 and td is None:  # 当此页没有能解析完成时，继续解析当前页，不翻页
            new_url = response.url
            return Request(url=new_url, callback=self.parse)
        elif self.total_count == 0 and td is not None:
            if len(td) > 0:
                _str = td[0].text.split('/')[1]
                self.total_count = int(''.join([x for x in _str if x.isdigit()]))


        # 处理数据
        self.set_data(body)
        # 准备下一页
        self.count += 1
        sleep(0.5)  # 防止启动过快

        if self.count <= self.total_count:
            new_url = self.url.format(self.config_list[self.config_count]) + "&page={0}".format(self.count)
            print('page:'+new_url)
            yield Request(url=new_url, callback=self.parse)
        elif self.config_count < (len(self.config_list)-1):  # 当一个关键字查询处理结束以后，开始下一个关键字处理
            self.config_count += 1
            self.count = 1
            self.total_count = 0
            # 参数重置之后，启动下一个配置查询
            new_url = self.url.format(self.config_list[self.config_count]) + "&page=1"
            print('keyword:'+new_url)
            yield Request(url=new_url, callback=self.parse)
        else:
            return

    def set_data(self, html):
        tr_list = html.xpath('//table[@class="msgtab"]/tbody/tr')
        sqlhelp = Dbsfda()
        data = []
        for tr in tr_list:  # 解析HTML
            td_list = tr.xpath("./td")
            if len(td_list) > 0:
                item = SFDAItem()
                item.xu_hao = td_list[0].text
                item.yao_pin_name = td_list[1].xpath("./a")[0].text
                item.pi_zhun_num = td_list[2].text
                item.sheng_chan_company = td_list[3].xpath("./a")[0].text
                item.zhi_ji = td_list[4].text
                item.gui_ge = td_list[5].text
                data.append(item)

        sqlhelp.add_list(data)  # 插入数据库

