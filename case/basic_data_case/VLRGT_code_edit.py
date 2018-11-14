#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
 VLRGT码 编辑
"""
log=Log()
class Vlrgt_code(unittest.TestCase):
    def setUp(self):
        print("VLRGT码编辑：开始测试")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        print("VLRGT码编辑：结束测试")
        self.driver.close()

    def edit(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[48]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_edit_empty(self):
        """不选直接编辑"""
        self.edit()
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name="请选择要修改的行"
        self.assertEqual(fact_name,expect_name)

    def test_edit_more(self):
        """编辑多条提示"""
        self.edit()
        driver = self.driver
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        time.sleep(0.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "不要选择多个"
        self.assertEqual(fact_name, expect_name)

    def test_edit_one(self):
        """选单条直接编辑"""
        self.edit()
        driver = self.driver
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        text = driver.find_element_by_class_name("mailbox-controls").text.split("创建时间")[1]
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()

        self.driver.find_element_by_name("vlr_number").clear()
        self.driver.find_element_by_name("vlr_number").send_keys("12111")
        driver.find_element_by_xpath("//*[@id='updateSpecialNumber']/div[3]/div/div/div/input").click()
        driver.find_element_by_css_selector("#updateSpecialNumber > div:nth-child(3) > div > div")
        driver.find_element_by_xpath("//*[@id='updateSpecialNumber']/div[3]/div/div/dl/dd[2]").click()  # 选择省份
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='updateSpecialNumber']/div[4]/div/div/div/input").click()
        driver.find_element_by_css_selector("#updateSpecialNumber > div:nth-child(4) > div > div")
        driver.find_element_by_xpath("//*[@id='updateSpecialNumber']/div[4]/div/div/dl/dd[2]").click()  # 选择地市

        self.driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "修改成功"
        self.assertEqual(fact_name, expect_name)

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == 'VLRGT_code_del':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Vlrgt_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码删除功能",
#         description='测试报告',
#     )
#     runner.run(suite)