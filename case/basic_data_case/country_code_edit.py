#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
"""
1.待审核 不选数据直接编辑
2.已审核
3.已撤销

4.        选择一条直接
5.
6.

7.
8.
9.
"""
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
log=Log()
class Country_code(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def edit(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[44]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_edit_待审核_empty(self):
        log.info("待审核不选直接编辑")
        self.edit()
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name="请选择要修改的行"
        self.assertEqual(fact_name,expect_name)

    def test_edit_已审核_empty(self):
        log.info("已审核不选直接编辑")
        self.edit()
        driver = self.driver
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[2]").click()
        self.driver.implicitly_wait(30)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        self.driver.implicitly_wait(10)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "请在待审核或已撤销页面进行编辑操作"
        self.assertEqual(fact_name, expect_name)

    def test_edit_已撤销_empty(self):
        log.info("已撤销不选直接编辑 测试用例")
        self.edit()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[3]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "请选择要修改的行"
        self.assertEqual(fact_name, expect_name)

    def test_edit_待审核_success(self):
        log.info("待审核不选直接编辑 测试用例")
        self.edit()
        driver = self.driver
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        text = driver.find_element_by_class_name("mailbox-controls").text.split("国家代码")[2]
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()

        self.driver.find_element_by_id("update_country_code").clear()
        self.driver.find_element_by_id("update_country_code").send_keys("12111")
        self.driver.find_elements_by_tag_name("a")[5].click()
        time.sleep(1.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "修改成功"
        self.assertEqual(fact_name, expect_name)

    def test_edit_已撤销_success(self):
        log.info("已撤销编辑 测试用例")
        self.edit()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[3]").click()
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        text = driver.find_element_by_class_name("mailbox-controls").text.split("国家代码")[2]
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()

        self.driver.find_element_by_id("update_country_code").clear()
        self.driver.find_element_by_id("update_country_code").send_keys("1332111")

        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        self.driver.implicitly_wait(10)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.info(fact_name)
        expect_name = "修改成功"
        self.assertEqual(fact_name, expect_name)

if __name__ == '__main__':
    unittest.main()