#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
"""
spec特殊短号码
"""
log=Log()
class Spec_code(unittest.TestCase):
    def setUp(self):
        log.info("特殊短号码添加：打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("特殊短号码添加：关闭浏览器")
        driver = self.driver
        driver.close()

    def add(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[49]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        time.sleep(2)
        write=self.driver.find_elements_by_class_name("desktop-app")[49]
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_tag_name("iframe"))
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//i[starts-with(@title,'新增')]"))
        self.driver.find_element_by_xpath("//i[starts-with(@title,'新增')]").click()

    """添加非空校验"""
    def test_add_depnumber_zero(self):
        """添加输入框：特殊短号码为空校验"""
        self.add()
        driver = self.driver
        # time.sleep(2)
        WebDriverWait(driver,10).until(lambda driver:driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys(" ")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("四盒大平原")
        driver.find_element_by_name("dep_sort").send_keys("觥觥研发埠")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_zonecode_empty(self):
        """添加输入框：长途区号为空校验"""
        self.add()
        driver = self.driver
        # time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("32442")
        driver.find_elements_by_name("zone_code")[1].send_keys(" ")
        driver.find_element_by_name("dep_name").send_keys("四盒大平原")
        driver.find_element_by_name("dep_sort").send_keys("觥觥研发埠")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_depname_zero(self):
        """添加输入框：部门名称 为空校验"""
        self.add()
        driver = self.driver
        # time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("32442")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys(" ")
        driver.find_element_by_name("dep_sort").send_keys("觥觥研发埠")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name = "部门名称不能为空，且不能多于50个汉字"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_depsort_empty(self):
        """添加输入框：部门类别 为空校验"""
        self.add()
        driver = self.driver
        # time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("32442")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("四盒大平原")
        driver.find_element_by_name("dep_sort").send_keys(" ")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name = "部门类别不能为空，且不能多于50个汉字"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_address_zero(self):
        """添加输入框：具体地址 为空校验"""
        self.add()
        driver = self.driver
        # time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("0992211")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("四盒大平原")
        driver.find_element_by_name("dep_sort").send_keys("觥觥研发埠")
        driver.find_element_by_name("add_ress").send_keys(" ")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_saveSpecialNumber6_zero(self):
        """添加输入框：省份下拉框 为空校验"""
        self.add()
        driver=self.driver
        # time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("0992211")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("四盒大平原")
        driver.find_element_by_name("dep_sort").send_keys("觥觥研发埠")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        # driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        # time.sleep(2)
        # driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        # driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name=driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name="必填项不能为空"
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_saveSpecialNumber7_zero(self):
        """添加输入框：启用状态下拉框 为空校验"""
        self.add()
        driver=self.driver
        # time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("0992211")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("四盒大平原")
        driver.find_element_by_name("dep_sort").send_keys("觥觥研发埠")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()
        time.sleep(2)
        # driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        # time.sleep(2)
        # driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        # driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name=driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name="必填项不能为空"
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_exsits(self):
        """数据已存在"""
        self.add()
        driver=self.driver
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("12315")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("打假部门")
        driver.find_element_by_name("dep_sort").send_keys("防假冒类")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(1.5)
        fact_name=driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expe_name="该特殊短号码已经存在"
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_add_success(self):
        """添加成功"""
        self.add()
        driver=self.driver
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-title"))
        # log.info("添加弹出框：%s" % driver.find_element_by_class_name("layui-layer-title").text)
        driver.find_elements_by_name("dep_number")[1].send_keys("12348")
        driver.find_elements_by_name("zone_code")[1].send_keys("010")
        driver.find_element_by_name("dep_name").send_keys("市长投诉部门")
        driver.find_element_by_name("dep_sort").send_keys("投诉建议类")
        driver.find_element_by_name("add_ress").send_keys("地球北京市北京市海淀区西二旗上地六街东口得实大厦2349层")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(6) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[6]/div/div/dl/dd[2]").click()

        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/div/input").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#saveSpecialNumber > div:nth-child(7) > div > div")
        driver.find_element_by_xpath("//*[@id='saveSpecialNumber']/div[7]/div/div/dl/dd[2]").click()

        driver.find_elements_by_tag_name("a")[2].click()
        time.sleep(0.5)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expe_name="添加成功"  #添加成功
        log.debug(fact_name)
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

# if __name__ == 'Spec_code':
    # reporter_dir = r's.html'
    # re_open = open(reporter_dir, 'wb')
    # suite = unittest.TestLoader().loadTestsFromTestCase(Spec_code)
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream=re_open,
    #     title="FZweb3.1.2特殊短号码添加功能",
    #     description='测试报告',
    # )
    # runner.run(suite)