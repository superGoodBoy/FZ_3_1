#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
"""号码封停处置"""
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from CINTEL_FZWEB3_1_2_1.logger.log import *

log=Log()
class UntitledTestCaseTask2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        log.info("打开浏览器")
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=c4b589c5-63d7-422f-9298-c35541a34873")
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()
        self.assertEqual([], self.verificationErrors)

    def test_untitled_test_case_task2(self):
        self.driver.find_element_by_id("login_name").send_keys("ct_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_id("vcode").send_keys("8888")

        self.driver.find_element_by_name("login_form").submit()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        time.sleep(5)
        self.driver.find_element_by_xpath("//div[@id='taskOrder']/div[6]/div/i").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | index=0 | ]]
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_xpath("//button[@onclick='deliver()']").click()
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        self.driver.find_element_by_xpath("//button[@type='reset']").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | relative=parent | ]]
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True



if __name__ == "__main__":
    unittest.main()
