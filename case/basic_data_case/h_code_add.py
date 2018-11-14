#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.action_chains import ActionChains
"""

手机h码：
1. 为空
2. 为空
3. 为空
4. 为空
5. 空 输入

6,7,8,9,10
11.已存在省编号校验
12.已存在
15.添加成功
"""
log=Log()
class H_code(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def add(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[46]

        action=ActionChains(driver)
        time.sleep(2)
        write=self.driver.find_elements_by_class_name("desktop-app")[46]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_add_hcode_imis_empty(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys(" ")
        driver.find_element_by_id("save_hcode").send_keys("43244424")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        #省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="IMSI号段或者手机H码输入长度不得大于10位数字"
        self.assertEqual(fact_name,expect_name)

    def test_add_save_hcode_empty(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        driver.find_element_by_name("hcode_imis").send_keys("32444424")
        driver.find_element_by_id("save_hcode").send_keys(" ")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        #省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="IMSI号段或者手机H码输入长度不得大于10位数字"
        self.assertEqual(fact_name,expect_name)

    def test_add_operator_empty(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys("32444424")
        driver.find_element_by_id("save_hcode").send_keys("43244424")
        # 运营商_(¦3」∠)_
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        #省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)

    def test_add_province_empty(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver = self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys("32444424")
        driver.find_element_by_id("save_hcode").send_keys("43244424")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        # 省份选择
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_city_empty(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys("32444424")
        driver.find_element_by_id("save_hcode").send_keys("43244424")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        #省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)

    def test_add_status_0_empty(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys("32444424")
        driver.find_element_by_id("save_hcode").send_keys("43244424")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        #省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        # driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        # driver.find_element_by_class_name("layui-layer-btn.layui-layer-btn-")
        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)

    def test_add_exsits(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" %driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys("1333241")
        driver.find_element_by_id("save_hcode").send_keys("1333241")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        #省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write =driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()

        time.sleep(1)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name="数据已存在"
        self.assertEqual(fact_name,expect_name)

    def test_add_success(self):
        self.add()
        self.driver.implicitly_wait(30)
        driver = self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("进入添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_element_by_name("hcode_imis").send_keys("3244774424")
        driver.find_element_by_id("save_hcode").send_keys("4324442467")
        # 运营商_(¦3」∠)_
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[3]/div/div/dl/dd[2]").click()
        # 省份选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[4]/div/div/dl/dd[2]").click()
        # 地市选择
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[5]/div/div/dl/dd[2]").click()
        # shifou漫游
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div")
        driver.find_element_by_xpath("//*[@id='saveHCode']/div[6]/div/div/dl/dd[2]").click()

        click_btn = driver.find_elements_by_tag_name('a')[5]
        action = ActionChains(driver)
        time.sleep(2)
        write = driver.find_elements_by_tag_name('a')[5]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)

        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "添加成功"
        self.assertEqual(fact_name, expect_name)

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(H_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2手机Ｈ码添加功能",
#         description='测试报告',
#     )
#     runner.run(suite)