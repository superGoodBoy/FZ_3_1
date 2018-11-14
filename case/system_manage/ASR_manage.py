#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import unittest,time,re

log=Log()
class UntitledTestCaseLog(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=c49ecf92-18c2-4602-850b-e1f55984fb9b")
        self.accept_next_alert = True

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn= self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('asrpz')\"]")
        action=ActionChains(self.driver)
        write=self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('asrpz')\"]")
        action.move_to_element(write).perform()
        click_btn.click()
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | index=0 | ]]
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(2)
        # driver.find_element_by_xpath("//i[@onclick=\"appFunction('tsdhm')\"]").click()
        # driver.find_element_by_xpath("//i[@onclick=\"appFunction('')\"]").click()

    def test_save(self):
        self.login()
        self.driver.find_element_by_id("save").click()
        demo_div =self.driver.find_element_by_class_name("layui-layer-content")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "数据保存成功"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | relative=parent | ]]
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_sync(self):
        self.login()
        self.driver.find_element_by_id("synchronization").click()
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_link_text(u"确定"))
        self.driver.find_element_by_link_text(u"确定").click()

        self.driver.switch_to_default_content()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | relative=parent | ]]
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_restartASR(self):
        self.login()
        self.driver.find_element_by_tag_name("button").click()
        print(self.is_element_present(how=By.XPATH,what="//*[@id='layui-layer1']/div"))
        self.driver.switch_to_default_content()
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
