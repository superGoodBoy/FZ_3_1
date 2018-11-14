#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,xlrd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
log= Log()
time_now=newestdate()
year=time_now['year']
month=time_now['month']
class H_code(unittest.TestCase):
    def setUp(self):
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)

    def export(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[46]
        action = ActionChains(driver)
        write = self.driver.find_elements_by_class_name("desktop-app")[46]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_filetemplate_title(self):
        u'断言是否增加了文件，匹配国家代码模板表头'
        driver = self.driver
        self.export()
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_history, 1)

        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div/div/button[6]").click()
        time.sleep(5)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_now, 2)
        self.assertNotEqual(path_filenum_history, path_filenum_now)

        filename = filedata_time_level01(name_title="手机H码模板%s年"%year, title_len=31, path=r"C:\Users\renqiwei\Downloads")
        print(filename)
        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" % filename)
        sheet1 = data.sheet_by_index(0)
        row_data_0 = sheet1.row_values(0)
        row_data = row_data_0
        print("下载文档表头：", row_data)

        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()


    def test_readExcel(self):

        driver = self.driver
        self.export()
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_history)
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[5]").click()
        time.sleep(150)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)
        if month[:1] =='0':
            filename = filedata_time_level01(name_title="手机H码%s年0%s"%(year,int(month)), title_len=29, path=r"C:\Users\renqiwei\Downloads")
        elif month[:1]!='0':
            filename = filedata_time_level01(name_title="手机H码%s年%s"%(year,int(month)), title_len=29, path=r"C:\Users\renqiwei\Downloads")
        print(filename)
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]
        print("excel文件数据：", table._cell_values,
              "excel文件条数：", table._cell_values.__len__())

        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def tearDown(self):
        driver = self.driver
        driver.quit()
if __name__ == '__main__':
    unittest.main()