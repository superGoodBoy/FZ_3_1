#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
添加时 国家代码，国家名称 根据id ，name元素定位，clear，click获取光标，js请求输入不进去，但可以定位
国家代码：
1.输入国家代码为空
2.输入国家名称为空
3.输入首都名称为空
4.输入经纬度为空
5.输入已有的国家代码是否能够保存
6.输入已有的国家名称，首都，国家代码不同是否能够保存
7.输入已存在的经纬度是否保存成功
8.输入一个正确的保存成功

"""
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

    def add(self):
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

    def test_add_countrycode_empty(self):
        self.add()
        driver=self.driver
        self.driver.find_element_by_css_selector(
            "body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        driver.find_elements_by_name("country_code")[1].send_keys(" ")
        driver.find_elements_by_name("country_name")[1].send_keys("空闲码")
        driver.find_element_by_name("capital").send_keys("空闲码")
        driver.find_element_by_name("capital_coordinate").send_keys("[2,2333]")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_countryname(self):
        self.add()
        driver = self.driver
        self.driver.find_element_by_css_selector(
            "body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        driver.find_elements_by_name("country_code")[1].send_keys("23234")
        driver.find_elements_by_name("country_name")[1].send_keys(" ")
        driver.find_element_by_name("capital").send_keys("空闲码")
        driver.find_element_by_name("capital_coordinate").send_keys("[2,2333]")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_capital_empty(self):
        self.add()
        driver = self.driver
        # self.driver.find_element_by_xpath(".//button[contains(text(),'添加')]")
        self.driver.find_element_by_css_selector("body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        driver.find_elements_by_name("country_code")[1].send_keys("23234")
        driver.find_elements_by_name("country_name")[1].send_keys("空闲码")
        driver.find_element_by_name("capital").send_keys(" ")
        driver.find_element_by_name("capital_coordinate").send_keys("[2,33]")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_capitalcoordinate_empty(self):
        self.add()
        driver = self.driver
        self.driver.find_element_by_css_selector(
            "body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        driver.find_elements_by_name("country_code")[1].send_keys("23234")
        driver.find_elements_by_name("country_name")[1].send_keys("空闲码")
        driver.find_element_by_name("capital").send_keys("空闲码")
        driver.find_element_by_name("capital_coordinate").send_keys(" ")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_exsits(self):
        self.add()
        driver = self.driver
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        self.driver.find_element_by_css_selector(
            "body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        driver.find_elements_by_xpath("//*[@id='country_code']")[1].send_keys("00591")
        driver.find_elements_by_xpath("//*[@id='country_name']")[1].send_keys("玻利维亚")
        driver.find_element_by_name("capital").send_keys("拉巴斯")
        driver.find_element_by_name("capital_coordinate").send_keys("[2,2333]")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(2)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "已经存在此国家代码"
        self.assertEqual(fact_name, expect_name)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_success(self):
        self.add()
        driver = self.driver
        self.driver.find_element_by_css_selector(
            "body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        driver.find_elements_by_xpath("//*[@id='country_code']")[1].send_keys("11100187")
        driver.find_elements_by_xpath("//*[@id='country_name']")[1].send_keys("火星省")
        driver.find_element_by_name("capital").send_keys("火星村")
        driver.find_element_by_name("capital_coordinate").send_keys("[233,233433]")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg"))
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "添加成功"
        self.assertEqual(fact_name, expect_name)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Country_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码添加功能",
#         description='测试报告',
#     )
#     runner.run(suite)