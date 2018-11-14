#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.action_chains import ActionChains
"""

长途区号：
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
class Area_code(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        url = "http://192.168.10.148:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def add(self):
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])

        click_btn = self.driver.find_elements_by_class_name("desktop-app")[45]
        action=ActionChains(self.driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        time.sleep(5)
        self.driver.find_element_by_xpath("//i[starts-with(@title,'新增')]").click()


    def test_add_areacode_empty(self):
        log.info("长途区号输入为空执行用例")
        self.add()
        driver=self.driver

        driver.find_elements_by_name("areacode")[1].send_keys(" ")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲码")
        driver.find_element_by_name("area_coordinate").send_keys("[2,34]")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲码")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)

    def test_add_areaname_empty(self):
        log.info("areaname为空执行用例")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("322323")
        driver.find_elements_by_name("areaname")[1].send_keys(" ")
        driver.find_element_by_name("area_coordinate").send_keys("[2,34]")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲码")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_areacoordinate_empty(self):
        log.info("坐标输入为空执行用例")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("3232311")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲码")
        driver.find_element_by_name("area_coordinate").send_keys(" ")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲码")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_provincecode_empty(self):
        log.info("省份输入为空用例执行")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("3232311")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲码")
        driver.find_element_by_name("area_coordinate").send_keys("[2,2434]")
        driver.find_element_by_name("provincecode").send_keys(" ")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲省份")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_saveAreaCodeId_empty(self):
        log.info("省份名称不能为空用例开始执行")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("3232311")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲码")
        driver.find_element_by_name("area_coordinate").send_keys("[2,34]")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys(" ")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_areacode_rule(self):
        log.info("长途区号输入规则校验")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("暗室逢灯")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲码")
        driver.find_element_by_name("area_coordinate").send_keys("[2,34]")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲省份")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "长途区号必须是数字编码"
        self.assertEqual(fact_name, expect_name)

    def test_add_areaname_rule(self):
        log.info("长途名称规则输入校验")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("123123")
        driver.find_elements_by_name("areaname")[1].send_keys("123131")
        driver.find_element_by_name("area_coordinate").send_keys("[2,34]")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲省份")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        time.sleep(1)
        fact_name=driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "不符合中文名称要求"
        self.assertEqual(fact_name, expect_name)

    def test_add_setcode_rule(self):
        log.info("局点编号添加 规则校验")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("123123")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲省份")
        driver.find_element_by_name("area_coordinate").send_keys("32424,23")
        driver.find_element_by_name("provincecode").send_keys("323232")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲省份")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "不符合坐标规范,格式为[xxx,xxx]"
        self.assertEqual(fact_name, expect_name)

    def test_add_provincecode_rule(self):
        log.info("省份编号输入规则校验")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("123123")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲省份")
        driver.find_element_by_name("area_coordinate").send_keys("[23,22]")
        driver.find_element_by_name("provincecode").send_keys("大家啊搜od")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("空闲省份")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "省份编号必须为数字编码"
        self.assertEqual(fact_name, expect_name)

    def test_add_province_rule(self):
        log.info("省份名称输入规则校验")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("123123")
        driver.find_elements_by_name("areaname")[1].send_keys("空闲省份")
        driver.find_element_by_name("area_coordinate").send_keys("[23,22]")
        driver.find_element_by_name("provincecode").send_keys("2342")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("2323")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()

        time.sleep(1)
        fact_name = driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expect_name = "不符合中文名称要求"
        self.assertEqual(fact_name, expect_name)

    def test_add_areacode_exists(self):
        log.info("长途区号已存在用例开始执行")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("77777")
        driver.find_elements_by_name("areaname")[1].send_keys("渥太华省")
        driver.find_element_by_name("area_coordinate").send_keys("[23,22]")
        driver.find_element_by_name("provincecode").send_keys("3333")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("渥太华市")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name=driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "长途区号或者地市已存在"
        self.assertEqual(fact_name,expect_name)

    def test_add_province_(self):
        log.info("省编码已被占用,请重新输入省编码")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("5558")
        driver.find_elements_by_name("areaname")[1].send_keys("美国")
        driver.find_element_by_name("area_coordinate").send_keys("[233,222]")
        driver.find_element_by_name("provincecode").send_keys("4444")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("野三坡")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(1)
        fact_name=driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "省编码已被占用,请重新输入省编码"
        self.assertEqual(fact_name, expect_name)

    def test_add_success(self):
        log.info("长途区号 添加成功用例执行：偶尔定位不到添加　按耨")
        self.add()
        driver = self.driver

        driver.find_elements_by_name("areacode")[1].send_keys("12123")
        driver.find_elements_by_name("areaname")[1].send_keys("伽玛省")
        driver.find_element_by_name("area_coordinate").send_keys("[23,22]")
        driver.find_element_by_name("provincecode").send_keys("245")
        driver.find_element_by_xpath("//*[@id='saveAreaCodeId']/div[5]/div/input").send_keys("伽玛市")
        driver.find_element_by_xpath("//html/body/div[3]/div[3]/a[1]").click()
        time.sleep(3)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "添加成功"
        self.assertEqual(fact_name, expect_name)

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