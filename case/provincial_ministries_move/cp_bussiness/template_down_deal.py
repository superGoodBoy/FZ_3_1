#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren

import unittest, time, re
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.by import By
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
class Cp_business_templetdown(unittest.TestCase):
    " cp_business_templetdown（省平台模板上行处置表）"

    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web/")
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.close()
        log.info("关闭浏览器")

    def login(self):
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])

        click_btn = self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('ywjhl')\"]")
        action = ActionChains(self.driver)
        write = self.driver.find_element_by_xpath("/html/body/div/div[3]/div[1]/div[7]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        for i in range(5):
            time.sleep(1)
            log.info("倒计时%s" % (5 - i))
        log.info(self.driver.find_element_by_xpath("/html/body/div/ul/li[3]").text)
        self.driver.find_element_by_xpath("/html/body/div/ul/li[3]").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-tab-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(3)

    def test_query_status(self):
        self.login()
        fact_name = []

        fact_name.append(int(self.driver.find_element_by_id("totalRecord_not_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealError").text))

        expe_name = []
        db = Mysql(dbconfig)
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='1=1 and status=0')[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='1=1 and status=1')[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='1=1 and status=2')[0][0])
        db.close()
        log.debug("%s,%s" % (fact_name, expe_name))
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_serialnumber(self):
        self.login()
        task = '0000001'
        fact_name = []

        self.driver.find_element_by_id("serial_number").send_keys(task)
        self.driver.find_element_by_class_name("layui-icon").click()
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_not_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealError").text))

        expe_name = []
        db = Mysql(dbconfig)
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='serial_number="%s" and 1=1 and status=0' % task)[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='serial_number="%s" and 1=1 and status=1' % task)[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='serial_number="%s" and 1=1 and status=2' % task)[0][0])
        db.close()
        log.debug("%s,%s" % (fact_name, expe_name))
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_date(self):
        self.login()
        fact_name = []

        his = "2018-01-01"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("totalRecord_not_dealSuccess"))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_not_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealError").text))

        expe_name = []
        db = Mysql(dbconfig)
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='create_time > "%s" and create_time <"%s" and 1=1 and status=0' % (
                                   his, now))[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='create_time > "%s" and create_time <"%s" and 1=1 and status=1' % (
                                   his, now))[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='create_time > "%s" and create_time <"%s" and 1=1 and status=2' % (
                                   his, now))[0][0])
        db.close()
        log.debug("%s,%s" % (fact_name, expe_name))
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_numrule(self):
        self.login()
        fact_name = []

        self.driver.find_element_by_css_selector("#conditionForm>div.selectArea>div:nth-child(2)>div>div>div>input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div/dl/dd[2]").click()
        self.driver.find_element_by_class_name("layui-icon").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("totalRecord_not_dealSuccess"))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_not_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealSuccess").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_dealError").text))

        expe_name = []
        db = Mysql(dbconfig)
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='dispose_type =0 and 1=1 and status=0')[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='dispose_type =0 and 1=1 and status=1')[0][0])
        expe_name.append(db.select(table='cp_business_templetdown', colume='count(DISTINCT serial_number)',
                                   condition='dispose_type =0 and 1=1 and status=2')[0][0])
        db.close()
        log.debug("%s,%s" % (fact_name, expe_name))
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealSuccess_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//i[@onclick='dealSuccess()']").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请选择要审批的行"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealSuccess2_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//li[@onclick='li_2()']").click()
        self.driver.find_element_by_xpath("//i[@onclick='dealSuccess()']").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请在待处置页面进行审批通过操作"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealSuccess3_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//li[@onclick='li_3()']").click()
        self.driver.find_element_by_xpath("//i[@onclick='dealSuccess()']").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请选择要处置的行"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealError_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//i[@onclick='dealError()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请选择要审核不通过的行"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealError2_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//li[@onclick='li_2()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//i[@onclick='dealError()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请在待处置页面进行审批不通过操作"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealError3_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//li[@onclick='li_3()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//i[@onclick='dealError()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请在待处置页面进行审批不通过操作"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealSuccess_success(self):
        self.login()

        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("//i[@onclick='dealSuccess()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "审核通过成功"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealsuccess3_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//li[@onclick='li_3()']").click()
        self.driver.find_element_by_xpath("//i[@onclick='dealSuccess()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请在待处置页面进行审批通过操作"
        self.assertEqual(fact_name, expe_name)

    def test_dealErrorreason_empty(self):
        self.login()

        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("//i[@onclick='dealError()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_id("desc").send_keys("")
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请输入审核意见"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()


    def test_dealError_success(self):
        self.login()

        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("//i[@onclick='dealError()']").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_id("desc").send_keys("审核不通过")
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "审核bu通过成功"
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_dealError3_empty(self):
        self.login()

        self.driver.find_element_by_xpath("//li[@onclick='li_3()']").click()

        # ----此处选中复选框

        self.driver.find_element_by_xpath("//i[@onclick='dealError()']").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name = "请选择要审核不通过的行"
        self.assertEqual(fact_name, expe_name)

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
