#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
"""统计数据推送"""

import unittest, time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
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
class Police_numberclosure(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web")
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.close()
        log.info("打开浏览器")
        self.assertEqual([], self.verificationErrors)

    def login(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        self.driver.implicitly_wait(30)
        click_btn =self.driver.find_element_by_xpath("//*[@id='police']/div[4]/div/i")
        action = ActionChains(self.driver)
        write =self.driver.find_element_by_xpath("//*[@id='police']/div[4]/div/i")
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        self.driver.implicitly_wait(30)

    def test_query(self):
        self.login()
        time.sleep(3)
        fact_text=self.driver.find_element_by_class_name("layui-laypage-count").text
        fact_text=int(re.findall(r"\d+\.?\d*",fact_text)[0]) #\d 匹配数字  \.[匹配除换行符任意字符
        print(fact_text)
        db=Mysql(dbconfig)
        expe_text=db.select(table='police_statistics',colume='batchno',condition='push_status=0 or push_status=1').__len__()
        db.close()
        self.assertEqual(fact_text,expe_text)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_date(self):
        self.login()
        time.sleep(3)

        now = time.strftime("%Y-%m-%d")
        his = "1990-05-05"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        WebDriverWait(self.driver,10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        fact_text = self.driver.find_element_by_class_name("layui-laypage-count").text
        fact_text = int(re.findall(r"\d+\.?\d*", fact_text)[0])  # \d 匹配数字  \.[匹配除换行符任意字符
        print(fact_text)
        db = Mysql(dbconfig)
        expe_text = db.select(table='police_statistics', colume='batchno',condition='push_status=0 or push_status=1').__len__()
        db.close()
        self.assertEqual(fact_text, expe_text)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_filename(self):
        self.login()
        time.sleep(3)
        name= 'filename'
        self.driver.find_element_by_name("statistics_file_name").send_keys(name)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        fact_text = self.driver.find_element_by_class_name("layui-laypage-count").text
        fact_text = int(re.findall(r"\d+\.?\d*", fact_text)[0])  # \d 匹配数字  \.[匹配除换行符任意字符
        print(fact_text)
        db = Mysql(dbconfig)
        expe_text = db.select(table='police_statistics', colume='batchno',
                              condition='statistics_file_name="%s"'%name).__len__()
        db.close()
        self.assertEqual(fact_text, expe_text)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
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
