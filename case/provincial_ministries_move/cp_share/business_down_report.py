#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-

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

dbconfig = {
    'host': '192.168.2.87',
    'port': 3306,
    'db': 'rg_web3_1',
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8'
}

log = Log()
class business_down_report(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml")
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])

        click_btn = self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('xxtbl')\"]")
        action = ActionChains(self.driver)
        write = self.driver.find_element_by_xpath("/html/body/div/div[3]/div[1]/div[7]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        for i in range(2):
            time.sleep(1)
            log.info("倒计时%s" % (2 - i))

    def test_queryDATE_cp_notify_info(self):
        """cp_notify_infomationdown（信息通告下发）"""
        self.login()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(
            re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_infomationdown', 'serial_number',
                              'create_time>="%s" and create_time <="%s" GROUP BY task_id ORDER BY create_time' % (his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_notify_info(self):
        """cp_notify_info（国家平台-信息通告下发表  暂为启用）"""
        self.login()
        tak = "22222"
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        try:
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as e:
            print(e)

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_infomationdown', 'serial_number', 'task_id="%s" group by task_id' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_notify_businessstatUP(self):
        """cp_notify_businessstat（业务统计数据记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('2')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(
            re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_businessstat', 'serial_number',
                              'create_time>="%s" and create_time <="%s" and resource=2 GROUP BY task_id ORDER BY create_time' % (
                              his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_notify_businessstatUP(self):
        """cp_notify_businessstat（业务统计数据记录表）"""
        self.login()
        tak = "201803030400001101031140"
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('2')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        try:
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as e:
            print(e)

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_businessstat', 'serial_number', 'task_id="%s" and resource=2 group by task_id' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_notify_businessstat(self):
        """cp_notify_businessstat（业务统计数据记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(
            re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_businessstat', 'serial_number',
                              'create_time>="%s" and create_time <="%s" and resource=1 GROUP BY task_id ORDER BY create_time' % (
                              his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_notify_businessstat(self):
        """cp_notify_businessstat（业务统计数据记录表）"""
        try:
            self.login()
            tak = "201803040610000001041003"
            self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
            self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
            self.driver.find_element_by_name("task_id").send_keys(tak)
            self.driver.find_element_by_class_name("layui-icon").click()
            self.driver.implicitly_wait(30)

            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

            db = Mysql(dbconfig)
            expe_name = db.select('cp_notify_businessstat', 'serial_number', 'task_id="%s" and resource=1 group by task_id' % tak).__len__()
            db.close()
            self.assertEqual(fact_name, expe_name)
            self.driver.switch_to_default_content()
            self.driver.switch_to_default_content()
            self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
            self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
            self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except NoSuchElementException as e:
            print(e)

    def test_queryDATE_cp_notify_businessstat(self):
        """cp_notify_businessstat（业务统计数据记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_queryDATE_cp_notify_interceptednum(self):
        """ cp_notify_interceptednum（号码拦截统计数据上报记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('5')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(
            re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_interceptednum', 'serial_number',
                              'create_time>="%s" and create_time <="%s" and resource=1 GROUP BY task_id ORDER BY create_time' % (
                                  his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_notify_interceptednum(self):
        """ cp_notify_interceptednum（号码拦截统计数据上报记录表）"""
        try:
            self.login()
            tak = "20180531013107174001"
            self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('5')\"]").click()
            self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
            WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_name("serial_number"))
            self.driver.find_element_by_name("serial_number").send_keys(tak)
            self.driver.implicitly_wait(30)
            log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            self.driver.find_elements_by_class_name("layui-icon")[0].click()
            self.driver.implicitly_wait(30)
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
            db = Mysql(dbconfig)
            expe_name = db.select('cp_notify_interceptednum', 'serial_number',
                                  ' serial_number ="%s" group by serial_number order by create_time' % tak).__len__()
            db.close()
            self.assertEqual(fact_name, expe_name)
            self.driver.switch_to_default_content()
            self.driver.switch_to_default_content()
            self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
            self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
            self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except NoSuchElementException as e:
            print(e)

    def test_queryDATE_cp_notify_interceptedtemplet(self):
        """ cp_notify_interceptedtemplet（模板拦截统计数据上报记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('3')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(
            re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_interceptedtemplet', 'serial_number',
                              'create_time>="%s" and create_time <="%s" group by task_id order by create_time' % (
                                  his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_notify_interceptedtemplet(self):
        """ cp_notify_interceptedtemplet（号码拦截统计数据上报记录表）"""
        try:
            self.login()
            tak = "44234234"
            self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('3')\"]").click()
            self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("task_id"))
            self.driver.find_element_by_name("task_id").send_keys(tak)
            self.driver.implicitly_wait(30)
            log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            self.driver.find_elements_by_class_name("layui-icon")[0].click()
            self.driver.implicitly_wait(30)
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
            db = Mysql(dbconfig)
            expe_name = db.select('cp_notify_interceptedtemplet', 'serial_number',
                                  'task_id="%s" group by task_id order by create_time' % tak).__len__()
            db.close()
            self.assertEqual(fact_name, expe_name)
            self.driver.switch_to_default_content()
            self.driver.switch_to_default_content()
            self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
            self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
            self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except NoSuchElementException as e:
            print(e)

    def test_queryDATE_cp_notify_fileup(self):
        """ cp_notify_fileup """
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(
            re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_notify_fileup', 'serial_number',
                              'create_time>="%s" and create_time <="%s" GROUP BY task_id ORDER BY create_time' % (
                                  his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_notify_fileup(self):
        """ cp_notify_interceptednum（号码拦截统计数据上报记录表）"""
        try:
            self.login()
            tak = "201804181021050601032752"
            self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
            self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            self.driver.find_element_by_name("task_id").send_keys(tak)
            self.driver.implicitly_wait(30)
            log.debug(self.driver.find_elements_by_class_name("layui-icon")[1].get_attribute("title"))
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            self.driver.find_elements_by_class_name("layui-icon")[1].click()
            self.driver.implicitly_wait(30)
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
            db = Mysql(dbconfig)
            expe_name = db.select('cp_notify_fileup', 'serial_number',
                                  'task_id ="%s" group by task_id order by create_time' % tak).__len__()
            db.close()
            self.assertEqual(fact_name, expe_name)
            self.driver.switch_to_default_content()
            self.driver.switch_to_default_content()
            self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
            self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
            self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except NoSuchElementException as e:
            print(e)

    def test_add_dateempty_cp_notify_fileup(self):
        """ cp_notify_interceptednum（号码拦截统计数据上报记录表）"""

        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))

        log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        self.driver.find_elements_by_class_name("layui-icon")[0].click()

        # now = time.strftime("%Y-%m-%d")
        # js = 'document.getElementById("file_date").value="%s 00:00:00"' % now
        # self.driver.execute_script(js)
        self.driver.find_element_by_name("file_unit").send_keys("保家大院")
        self.driver.find_element_by_name("remark").send_keys("保家大院描述")

        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_add_file_unitempty_cp_notify_fileup(self):
        """ cp_notify_interceptednum（号码拦截统计数据上报记录表）"""

        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))

        log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        self.driver.find_elements_by_class_name("layui-icon")[0].click()

        now =time.strftime("%Y-%m-%d")
        js='document.getElementById("file_date").value="%s 00:00:00"'%now
        self.driver.execute_script(js)
        self.driver.find_element_by_name("file_unit").send_keys("")
        self.driver.find_element_by_name("remark").send_keys("fasf")

        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_add_remarkempty_cp_notify_fileup(self):
        """ cp_notify_interceptednum（号码拦截统计数据上报记录表）"""

        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))

        log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        self.driver.find_elements_by_class_name("layui-icon")[0].click()

        now =time.strftime("%Y-%m-%d")
        js='document.getElementById("file_date").value="%s 00:00:00"'%now
        self.driver.execute_script(js)
        self.driver.find_element_by_name("file_unit").send_keys("fasf")
        self.driver.find_element_by_name("remark").send_keys("")

        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_add_exsits_cp_notify_fileup(self):
        """  """

        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))

        log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        self.driver.find_elements_by_class_name("layui-icon")[0].click()

        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("file_date").value="%s 00:00:00"' % now
        self.driver.execute_script(js)
        self.driver.find_element_by_name("file_unit").send_keys("fasf")
        self.driver.find_element_by_name("remark").send_keys("")

        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "已存在"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_add_success_cp_notify_fileup(self):
        """  """

        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))

        log.debug(self.driver.find_elements_by_class_name("layui-icon")[0].get_attribute("title"))
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        self.driver.find_elements_by_class_name("layui-icon")[0].click()

        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("file_date").value="%s 00:00:00"' % now
        self.driver.execute_script(js)
        self.driver.find_element_by_name("file_unit").send_keys("fasf")
        self.driver.find_element_by_name("remark").send_keys("")

        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "添加成功"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
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
