#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-

import unittest, time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from selenium.webdriver.common.action_chains import ActionChains
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
log=Log()
class Cp_business_templetup(unittest.TestCase):
    " cp_business_templetup（省平台模板上行处置表）"
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
        self.driver.find_element_by_id("Img").text
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
        for i in range(3):
            time.sleep(1)
            log.info("倒计时%s" % (3 - i))
        log.info(self.driver.find_element_by_xpath("/html/body/div/ul/li[2]").text)
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-tab-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        for i in range(3):
            time.sleep(1)
            log.info("倒计时%s" % (3 - i))

    def test_addsuccess(self):
        """添加失败,需要布置转码程序"""
        pass

    def test_add_fileempty(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()

        self.driver.find_element_by_id("test8")#点击事件
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[2]/i").click()
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[3]/div/div[6]/i").click()#来源 选择通管
        self.driver.find_element_by_xpath("//*[@id='sheng']/div[1]/i").click()
        js= 'document.getElementById("dispose_end").value="2018-06-11 00:00:00"'
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name="请选择文件"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_add_dateempty(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()

        self.driver.find_element_by_id("test8")  # 点击事件
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[2]/i").click()
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[3]/div/div[6]/i").click()  # 来源 选择通管
        self.driver.find_element_by_xpath("//*[@id='sheng']/div[1]/i").click()
        js = 'document.getElementById("dispose_end").value="2018-06-11 00:00:00"'
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "请选择文件"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_add_disposereason_empty(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()

        self.driver.find_element_by_id("test8")  # 点击事件
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[2]/i").click()
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[3]/div/div[6]/i").click()  # 来源 选择通管
        self.driver.find_element_by_xpath("//*[@id='sheng']/div[1]/i").click()
        js = 'document.getElementById("dispose_end").value="2018-06-11 00:00:00"'
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name = "请选择文件"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_empty(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]").click()
        time.sleep(1)
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name="请选择要删除的行"
        self.assertEqual(expe_name,fact_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_success(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]").click()
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        # WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_css_selector("#layui-layer4 > span.layui-layer-setwin > a"))
        time.sleep(1)
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name="删除模板上行处置任务成功"
        self.assertEqual(expe_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_export_document(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[4]").click()
        filename = filedata_time_level01(name_title="模板上行处置2018年", title_len=31, path=r"C:\Users\renqiwei\Downloads")
        WebDriverWait(self.driver, 10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name=self.driver.find_element_by_class_name("layui-layer-content").text
        time.sleep(4)
        expe_name="导出模板数据成功"
        self.assertEqual(fact_name,expe_name)
        log.info(filename)
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)

        sheet1 = data.sheet_by_index(0)
        row_data_0 = sheet1.row_values(0)
        row_data = row_data_0
        print(row_data)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_report(self):
        self.login()
        self.driver.find_elements_by_class_name("layui-icon")[4].click()
        WebDriverWait(self.driver, 10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content"))
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name = "请选择要上报的行"
        self.assertEqual(fact_name,expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_reportquery(self):
        self.login()
        self.driver.find_elements_by_class_name("iconfont")[3].click()

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_import_temlete(self):
        self.login()
        self.driver.find_element_by_class_name("layui-icon")
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[5]/div[2]").click()
        pass

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

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
