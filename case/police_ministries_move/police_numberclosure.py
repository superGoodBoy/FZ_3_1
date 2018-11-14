#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
"""诈骗号码封停"""

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
        log.info("打开浏览器")
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http:\\192.168.2.87:8080/rg_web")

    def tearDown(self):
        self.driver.close()
        log.info("关闭浏览器")
        # self.assertEqual([], self.verificationErrors)

    def login(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        click_btn =  self.driver.find_element_by_xpath("//*[@id='police']/div[3]/div/i")
        action = ActionChains(self.driver)
        write = self.driver.find_element_by_xpath("//*[@id='police']/div[3]/div/i")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        self.driver.implicitly_wait(30)

    def test_export(self):
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        self.login()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button").click()

        time.sleep(7)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        self.assertNotEqual(path_filenum_history, path_filenum_now)
        filename = filedata_time_level01(name_title="诈骗号码封停2018年", title_len=31, path=r"C:\Users\renqiwei\Downloads")
        log.info(filename)
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]  # 说明能打开该文件
        nrows = table.nrows

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_deliver_1_empty(self):
        self.login()
        time.sleep(3)
        self.driver.find_element_by_xpath("//i[@onclick='deliver()']").click()  # 号码审批通过
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name = "请选择行！"
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_deliver_2_empty(self):
        self.login()
        time.sleep(3)
        self.driver.find_element_by_xpath("//li[@onclick='li_2()']").click()
        self.driver.find_element_by_xpath("//i[@onclick='deliver()']").click()  # 号码审批通过
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name = "请在待审核页面选择要审批的行"
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_deliver_1_success(self):
        self.login()
        time.sleep(3)

        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()  # qdiyige

        self.driver.find_element_by_xpath("//i[@onclick='deliver()']").click()
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-title"))
        log.info("审批确认框：%s" %self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        time.sleep(0.5)
        fact_name=self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name = "审批成功"
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_cancel_1_empty(self):
        self.login()
        time.sleep(3)
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_xpath("//i[@onclick='cancel()']").click()  # 号码审批不通过
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name = "请选择行！"
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_cancel_2_empty(self):
        self.login()
        time.sleep(3)
        self.driver.find_element_by_xpath("//li[@onclick='li_2()']").click()
        self.driver.find_element_by_xpath("//i[@onclick='cancel()']").click()  # 号码审批不通过
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name = "请在待审核页面选择要审批的行"
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_cancel_2_rule(self):
        self.login()
        time.sleep(2)
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("//i[@onclick='cancel()']").click()  # 号码审批不通过
        # self.driver.find_element_by_id("approopinionn").send_keys("不通过")
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name=self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name="必填项不能为空"
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click

    def test_cancel_2_success(self):
        self.login()
        time.sleep(2)
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("//i[@onclick='cancel()']").click()  # 号码审批不通过
        self.driver.find_element_by_id("approopinionn").send_keys("不通过")
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name=self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expe_name="审批通过"
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_date(self):
        self.login()
        time.sleep(3)
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        now = time.strftime("%Y-%m-%d")
        his = "1990-05-05"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        fact_name=[]
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_not_check").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_check").text))

        db = Mysql(dbconfig)
        expe_name=[]
        expe_name.append(db.select(table='police_numberclosure', colume='calling_number', condition='create_time >="%s"  and create_time <= "%s" and policepushstatus =1  and approstatus =0'%(his,now)).__len__())
        expe_name.append(db.select(table='police_numberclosure', colume='calling_number', condition='create_time >="%s"  and create_time <= "%s" and policepushstatus =1 and (approstatus =1 or approstatus =2)'%(his,now)).__len__())
        db.close()
        log.info("%s ,%s" %(expe_name,fact_name))
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_batchno(self):
        self.login()
        time.sleep(2)
        ba="162D6797D5991F"
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_name("batchno").send_keys(ba)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        fact_name = int(self.driver.find_element_by_id("totalRecord_not_check").text)
        db = Mysql(dbconfig)
        expe_name=db.select(table='police_numberclosure', colume='calling_number', condition="batchno='%s'"%ba).__len__()
        db.close()
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_calling_number(self):
        self.login()
        time.sleep(2)
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_name("calling_number").send_keys("13520211401")
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        fact_name = int(self.driver.find_element_by_id("totalRecord_not_check").text)
        db = Mysql(dbconfig)
        expe_name=db.select(table='police_numberclosure', colume='calling_number', condition='calling_number="13520211401"').__len__()
        db.close()
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_operator(self):
        self.login()
        time.sleep(2)
        self.driver.find_element_by_xpath("//li[@onclick='li_1()']").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div")
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[4]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        fact_name=[]
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_not_check").text))
        fact_name.append(int(self.driver.find_element_by_id("totalRecord_check").text))
        db = Mysql(dbconfig)
        expe_name=[]
        expe_name.append(int(db.select(table='police_numberclosure', colume='calling_number', condition='belongcarrier=0 and policepushstatus =1 and approstatus = 0').__len__()))
        expe_name.append(int(db.select(table='police_numberclosure', colume='calling_number', condition='belongcarrier=0 and policepushstatus =1 and (approstatus =1 or approstatus =2)').__len__()))
        db.close()

        self.assertEqual(expe_name, fact_name)
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
