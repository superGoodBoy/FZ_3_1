#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
from selenium import webdriver
import unittest,time,re,redis
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from  CINTEL_FZWEB3_1_2_1.logger.log import *
"""
运行前请将192.168.2.51,130,52服务器的redis清空
---首先 对web页面初始化操作
1.对初始化成功后提示语校验
2.对redis数据及 mysql数据库对比
"""
log=Log()
class Area_code(unittest.TestCase):
    def setUp(self):
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def test_edit(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[45]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[7]").click()
        self.driver.implicitly_wait(30)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "成功初始化"
        self.assertEqual(fact_name, expect_name)
        # import redis
        # r = redis.Redis(host='192.168.2.51', port=7113)
        # import re
        # text_3 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("areacode_*")])))).split(" ")
        r = redis.Redis(host='192.168.2.51',port=7111)
        text_1=" ".join(re.findall(r"\d+\.?\d*"," ".join(sorted([str(i) for i in r.keys("areacode_*")])))).split(" ")
        r = redis.Redis(host='192.168.2.51', port=7112)
        text_2 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("areacode_*")])))).split(" ")

        r = redis.Redis(host='192.168.2.52', port=7111)
        text_3 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("areacode_*")])))).split(" ")
        r = redis.Redis(host='192.168.2.52', port=7112)
        text_4 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("areacode_*")])))).split(" ")

        text =text_1+text_2+text_3+text_4
        text=sorted(text)

        # log.debug("redis同步数据,%s" %text)
        log.debug("redis同步数据条数,%s" %text.__len__())
        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        fact_ = db.select(table="t_areacode", colume='areacode')
        fact = Mysql.make_list(fact_)
        log.debug(fact.__len__())
        # log.debug("mysql数据条数", fact.__len__())

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Country_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码添加功能",
#         description='测试报告',
#     )
#     runner.run(suite)