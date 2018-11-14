#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 09:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-

import unittest,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *

dbconfig = {
    'host': '192.168.2.87',
    'port': 3306,
    'db': 'rg_web3_1',
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8'
}

log=Log()
class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        log.info("打开浏览器")
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=65cc0fb4-3dd3-4c1f-94db-a167d1b66d39")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ca_system_admin")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("vcode").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])

        click_btn=driver.find_element_by_css_selector("#selectData>div:nth-child(3)>div")
        action = ActionChains(self.driver)
        write = driver.find_element_by_css_selector("#selectData>div:nth-child(3)>div")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))
        time.sleep(5)

    def test_export(self):
        self.login()
        self.driver.find_element_by_css_selector("body > div.box.box-primary > div:nth-child(3) > div.row-left > div > button:nth-child(3)").click()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(5)
        filename = filedata_time_level01(name_title="去灰号码2018年06", title_len=29, path=r"C:\Users\renqiwei\Downloads")
        print(filename)
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]
        log.debug("excel文件条数：%s" % table._cell_values.__len__())

if __name__ == "__main__":
    unittest.main()
