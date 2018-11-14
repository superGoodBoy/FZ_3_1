#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,xlrd
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.action_chains import ActionChains
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
log= Log()
class Vlrgt_code(unittest.TestCase):
    def setUp(self):
        print("VLRGT码导出：开始测试")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        print("VLRGT码导出：结束测试")
        self.driver.close()

    def import_vlrnumber(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])

        click_btn = self.driver.find_elements_by_class_name("desktop-app")[48]
        action = ActionChains(driver)
        write = self.driver.find_elements_by_class_name("desktop-app")[48]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_filetemplate_title(self):
        u'断言是否增加了文件，人工审核模板表头'
        # a="国家代码模板2018年05月07日12时10分23秒.xlsx"
        # print(a.__len__())
        driver = self.driver
        self.import_vlrnumber()
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_history, 1)

        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div/div/button[6]").click()
        time.sleep(5)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_now, 2)
        self.assertNotEqual(path_filenum_history, path_filenum_now)

        filename = filedata_time_level01(name_title="VLR number模", title_len=37, path=r"C:\Users\renqiwei\Downloads")
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
        u'断言是否增加了文件，人工审核数据'
        driver = self.driver
        self.import_vlrnumber()
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_history, 1)
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[5]").click()
        time.sleep(10)
        path_filenum_now = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_now, 2)
        self.assertNotEqual(path_filenum_history, path_filenum_now)

        filename = filedata_time_level01(name_title="VLR number2", title_len=35, path=r"C:\Users\renqiwei\Downloads")
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

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == 'VLRGT_code_export':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Vlrgt_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码导出功能",
#         description='测试报告',
#     )
#     runner.run(suite)