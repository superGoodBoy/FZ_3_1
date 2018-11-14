#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,xlrd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
log=Log()

year=newestdate()['year']
month=newestdate()['month']

class Space_code(unittest.TestCase):
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

    def import_depnumber(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[49]
        action = ActionChains(driver)
        write = self.driver.find_elements_by_class_name("desktop-app")[49]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        try:
            log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        except NoSuchElementException as e:
            print(e)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_filetemplate_title(self):
        u'断言是否增加了文件，人工审核表头'
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        self.import_depnumber()
        time.sleep(1)
        log.debug(path_filenum_history)
        time.sleep(2)

        self.driver.find_element_by_xpath("//i[starts-with(@title,'下载模板')]").click()
        time.sleep(10)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        log.debug(path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)

        filename = filedata_time_level01(name_title="特殊短号码模板%s" %year, title_len=32, path=r"C:\Users\renqiwei\Downloads")
        log.debug(filename)

        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" % filename)
        sheet1 = data.sheet_by_index(0)
        row_data_0 = sheet1.row_values(0)
        row_data = row_data_0
        log.debug("下载文档表头：%s"%row_data)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        # self.driver.find_element_by_xpath(".//li[@onclick='quit()']").click()
        # self.driver.find_element_by_css_selector("#person > ul > li:nth-child(3)").click()
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_readExcel(self):
        """断言是否增加了文件，人工审核内容"""
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        self.import_depnumber()
        log.info(path_filenum_history)
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[5]").click()
        time.sleep(15)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)
        if month[:1]=='0':
            filename = filedata_time_level01(name_title="特殊短号码%s年0" %(year), title_len=30, path=r"C:\Users\renqiwei\Downloads")
        elif month[:1] != '0':
            filename = filedata_time_level01(name_title="特殊短号码%s年%s" % (year, int(month[:1])), title_len=30,path=r"C:\Users\renqiwei\Downloads")
        print(filename)
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]
        # print("excel文件数据：", table._cell_values,)
        log.debug("excel文件条数：%s"%table._cell_values.__len__())

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//div[@onclick='togglePro()']"))
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")
if __name__ == '__main__':
    unittest.main()