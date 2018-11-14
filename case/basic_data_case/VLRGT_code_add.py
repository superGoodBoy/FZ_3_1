#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from CINTEL_FZWEB3_1_2_1.logger.log import *

"""

vlrgt添加

"""
log=Log()
class Vlrgt_code(unittest.TestCase):
    def setUp(self):
        log.info("vlrgt码添加：打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("vlrgt码添加：关闭浏览器")
        self.driver.close()

    def add(self):
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
        time.sleep(2)
        write=self.driver.find_elements_by_tag_name("legend")[5]
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_add_vlr_empty(self):
        """添加输入框：VLRGT码为空"""
        self.add()
        driver = self.driver
        self.driver.implicitly_wait(30)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_elements_by_name("vlr_number")[1].send_keys("  ")
        driver.find_elements_by_name("area_code")[1].send_keys("53453")

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(3) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/dl/dd[2]").click()  # 选择省份
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(4) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/dl/dd[2]").click()  # 选择地市

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(5) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/dl/dd[2]").click()  # 选择运营商

        # self.driver.find_element_by_class_name("layui-layer-btn0").click()
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(2)
        content_web = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(content_web)

        content_exp = "必填项不能为空"
        self.assertEqual(content_exp, content_web)

    def test_add_areacode_empty(self):
        """添加输入框：长途区号 为空"""
        self.add()
        driver = self.driver
        self.driver.implicitly_wait(30)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_elements_by_name("vlr_number")[1].send_keys("53453")
        driver.find_elements_by_name("area_code")[1].send_keys(" ")

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(3) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/dl/dd[2]").click()  # 选择省份
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(4) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/dl/dd[2]").click()  # 选择地市

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(5) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/dl/dd[2]").click()  # 选择运营商
        driver.implicitly_wait(30)
        driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        # driver.implicitly_wait(15)
        content_web = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(content_web)
        content_exp = "必填项不能为空"
        self.assertEqual(content_exp, content_web)

    def test_add_province_empty(self):
        """添加选择输入框：省份为空"""
        self.add()
        self.driver.implicitly_wait(30)
        driver = self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_elements_by_name("vlr_number")[1].send_keys("53453")
        driver.find_elements_by_name("area_code")[1].send_keys("32323")

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(5) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/dl/dd[2]").click()  # 选择运营商

        driver.find_element_by_class_name("layui-layer-btn0").click()
        # driver.implicitly_wait(15)
        time.sleep(0.5)
        content_web = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(content_web)
        content_exp = "必填项不能为空"
        self.assertEqual(content_exp, content_web)

    def test_add_operator_empty(self):
        """添加选择输入框：运营商选择为空"""
        self.add()
        self.driver.implicitly_wait(30)
        driver = self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_elements_by_name("vlr_number")[1].send_keys("53453")
        driver.find_elements_by_name("area_code")[1].send_keys("32323")

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(3) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/dl/dd[2]").click()  # 选择省份
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(4) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/dl/dd[2]").click()  # 选择地市

        # driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/div/input").click()
        # driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(5) > div > div")
        # driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/dl/dd[2]").click()  # 选择运营商

        driver.find_element_by_class_name("layui-layer-btn0").click()
        # driver.implicitly_wait(20)
        time.sleep(2)
        content_web = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(content_web)
        content_exp = "必填项不能为空"
        self.assertEqual(content_exp, content_web)

    def test_addvlr_exsits(self):
        """添加已存在测试"""
        self.add()
        self.driver.implicitly_wait(30)
        driver = self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_elements_by_name("vlr_number")[1].send_keys("0838")
        driver.find_elements_by_name("area_code")[1].send_keys("010")

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(3) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/dl/dd[2]").click()  # 选择省份
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(4) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/dl/dd[2]").click()  # 选择地市

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(5) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/dl/dd[2]").click()  # 选择运营商

        driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        content_web = driver.find_elements_by_class_name("layui-layer-content")[1].text
        content_exp = "该VLR_Number已经存在"
        self.assertEqual(content_exp, content_web)

    def test_addvlr_success(self):
        """添加成功:"""
        self.add()
        self.driver.implicitly_wait(30)
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        self.driver.implicitly_wait(30)
        driver.find_elements_by_name("vlr_number")[1].send_keys("11028")
        driver.find_elements_by_name("area_code")[1].send_keys("010")

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(3) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[3]/div/div/dl/dd[2]").click() #选择省份
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(4) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[4]/div/div/dl/dd[2]").click() #选择地市

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/div/input").click()
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(5) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[5]/div/div/dl/dd[2]").click()  # 选择运营商
        driver.find_element_by_class_name("layui-layer-btn0").click()

        time.sleep(2)
        # content_web=driver.find_elements_by_class_name("layui-layer-content")[1].text
        content_web=driver.find_element_by_xpath("/html/body/div[3]/div").text
        log.debug(content_web)
        content_exp="添加成功"
        self.assertEqual(content_exp,content_web)

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Vlrgt_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码添加功能",
#         description='测试报告',
#     )
#     runner.run(suite)



