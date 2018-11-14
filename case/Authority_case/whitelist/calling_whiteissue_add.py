#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# @Site    : 
# @File    : calling_whiteissue_add.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.logger.log import Log
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner

"""
测试用例：
1.添加号码超长
2.添加原因超长
3.添加号码非空
4.添加原因非空
5.添加号码特殊字符
6.添加原因特殊字符
7.已存在
7.添加成功

"""

data=[
    {"whitenum":"1851222223333333333333333333333242342123413423243333333","whitereason":"rqw"},
    {"whitenum":"18512223333","whitereason":"rqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqwrqw"},
    {"whitenum":"","whitereason":"rqw"},
    {"whitenum":"1851222223333333333333333333333333333","whitereason":""},
    {"whitenum":"@#@!#","whitereason":"rqw"},
    {"whitenum":"1851222223333333333333333333333333333","whitereason":"$@#$@我哦我哦问我"},
    {"whitenum":"010897773","whitereason":"rqw已存在"},
    {"whitenum":"010897774","whitereason":"rqw成功添加"}
]
log=Log()
class Addwhite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        url = 'http://192.168.2.87:8080/rg_web/index.shtml'
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def addwhite(self,addwhitenum,addwhitereason):
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_css_selector("div.login-btn").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])

        self.driver.find_element_by_xpath("//div[@id='taskOrder']/div[4]/div/i").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))
        time.sleep(1.5)
        self.driver.find_element_by_css_selector("div.layui-btn-group.site-demo-button > button.layui-btn.layui-btn-primary.layui-btn-small").click()
        self.driver.find_element_by_css_selector("div.layui-input-block>#calling_number").click()
        self.driver.find_element_by_css_selector("div.layui-input-block>#calling_number").send_keys(addwhitenum)
        self.driver.find_element_by_name("add_reason").send_keys(addwhitereason)
        time.sleep(1.5)
        self.driver.find_element_by_link_text(u"保存").click()

    def test_numtoolng(self):
        driver = self.driver
        data_0= data[0]
        addnum =data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum,addreason)
        time.sleep(1)
        fact_name=driver.find_element_by_css_selector("div.layui-layer-content.layui-layer-padding").text
        log.debug(fact_name)
        expect_name ="请输入号码1到30位数字"
        self.assertEqual(fact_name,expect_name)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        self.driver.find_element_by_css_selector("div.protel").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_reasontoolng(self):
        driver = self.driver
        data_0 = data[1]
        addnum = data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum, addreason)
        time.sleep(3)
        fact_name = driver.find_element_by_css_selector("div.layui-layer-content.layui-layer-padding").text
        log.debug(fact_name)
        time.sleep(1.5)
        expect_name = "输入原因不能为空且在50字符 以内 ！"
        self.assertEqual(fact_name, expect_name)

        driver.switch_to_default_content()
        driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        driver.find_element_by_css_selector("div.protel").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_numzero(self):
        driver = self.driver
        data_0 = data[2]
        addnum = data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum, addreason)
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector("div.layui-layer-content.layui-layer-padding").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

        driver.switch_to_default_content()
        driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        driver.find_element_by_css_selector("div.protel").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_reasonzero(self):
        driver = self.driver
        data_0 = data[3]
        addnum = data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum, addreason)
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector("div.layui-layer-content.layui-layer-padding").text
        log.debug(fact_name)
        expect_name = "请输入号码1到30位数字"
        self.assertEqual(fact_name, expect_name)

        driver.switch_to_default_content()
        driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        driver.find_element_by_css_selector("div.protel").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_numnot(self):
        driver = self.driver
        data_0= data[4]
        addnum =data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum,addreason)
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector("div.layui-layer-content.layui-layer-padding").text
        log.debug(fact_name)
        expect_name ="请输入号码1到30位数字"
        self.assertEqual(fact_name,expect_name)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        self.driver.find_element_by_css_selector("div.protel").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_reasonnot(self):
        driver = self.driver
        data_0 = data[5]
        addnum = data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum, addreason)
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector("div.layui-layer-content.layui-layer-padding").text
        log.debug(fact_name)
        expect_name = "请输入号码1到30位数字"
        self.assertEqual(fact_name, expect_name)

        driver.switch_to_default_content()
        driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        driver.find_element_by_css_selector("div.protel").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_numexists(self):
        driver = self.driver
        data_0= data[6]
        addnum =data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum,addreason)
        time.sleep(1)
        # fact_name1=driver.find_element_by_css_selector("#layui-layer2 > div.layui-layer-content").text
        fact_name = driver.find_element_by_xpath("/html/body/div[4]/div[2]").text
        log.debug(fact_name)
        expect_name ="白名单已经存在此号码:010897773"
        self.assertEqual(fact_name,expect_name)
        #
        driver.switch_to_default_content()
        driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        driver.find_element_by_css_selector("div.protel").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_numsuccess(self):
        driver = self.driver
        data_0= data[7]
        addnum =data_0['whitenum']
        addreason = data_0['whitereason']
        self.addwhite(addnum,addreason)
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name ="添加成功"
        self.assertEqual(fact_name,expect_name)

        driver.switch_to_default_content()
        driver.find_element_by_css_selector("a.layui-layer-ico.layui-layer-close.layui-layer-close1").click()
        time.sleep(1.5)
        driver.find_element_by_css_selector("div.protel").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Addwhite)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2功能",
#         description='测试报告',
#     )
#     runner.run(suite)
