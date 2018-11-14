#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 15:34
# @Author  : QiWei.Ren
# @Site    : 
# @File    : Reporter_exportDocument.py
# @Software: PyCharm
import unittest,xlrd
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *

log=Log()
class ExportDocument(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def export_Document(self):
        driver = self.driver
        time.sleep(3)
        driver.find_element_by_id("login_name").send_keys('ct_operator')
        driver.find_element_by_id("password").send_keys('123456')
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_css_selector("#taskOrder > div:nth-child(4) > div > span").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))

    def test_file_document(self):
        u"检查下载模板成功提示语,"
        path_filenum_history = nu(self, num=0, path=r"C:\Users\renqiwei\Downloads") - 1
        self.export_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[4]").click()
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        time.sleep(10)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = "主叫白名单导出成功！"
        self.assertEqual(fact_result, expect_result)
        path_filenum_now = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_history,fact_result,path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)
        filename = filedata_time_level01(name_title="主叫白名单号码-待推送", title_len=36, path=r"C:\Users\renqiwei\Downloads")
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]
        nrows = table.nrows
        print(nrows - 1)
        for i in range(nrows):
            if i > 0:
                if table.row_values(i)[0] == "":
                    u"导出的数据加灰号码不能为空"
                    print("导出的数据加灰号码不能为空")
                    self.assertNotEqual(table.row_values(i)[0], "")
                else:
                    if table.row_values(i)[3] == "":
                        u" 导出的数据加灰原因不能为空"
                        print("导出的数据加灰原因不能为空")
                        self.assertNotEqual(table.row_values(i)[3], "")
                    else:
                        print(table.row_values(i))
                        continue

    def test_file_temeplete(self):
        u"检查下载模板成功提示语,"
        self.export_Document()
        path_filenum_history = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads") - 1
        time.sleep(2)
        self.driver.find_element_by_xpath(u"/html/body/div[1]/div[1]/div[1]/div/button[5]").click()
        WebDriverWait(self.driver,10).until(lambda driver:driver.find_element_by_xpath("/html/body/div[2]/div"))
        fact_result = self.driver.find_element_by_xpath("/html/body/div[2]/div").text
        expect_result = "导出模板成功"
        self.assertEqual(fact_result, expect_result,fact_result)
        time.sleep(10)
        path_filenum_now = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads") - 1
        print(path_filenum_history,path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)
        # filename_now = filedata_list(self, num=0)
        filename = filedata_time_level01(name_title="主叫白名单号码模版20", title_len=34, path=r"C:\Users\renqiwei\Downloads")
        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" % filename)
        sheet1 = data.sheet_by_index(0)
        row_data_0 = sheet1.row_values(0)
        row_data = row_data_0[0]
        # print(row_data)
        row_data_expect1 = "主叫号码"
        assert row_data, row_data_expect1
        self.assertEqual(row_data, row_data_expect1)

        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" % filename)
        sheet1 = data.sheet_by_index(0)
        row_data = sheet1.row_values(0)
        print(row_data[1])
        row_data_expect2 = "加白原因"
        self.assertEqual(row_data[1], row_data_expect2)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(ImportDocument)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码功能",
#         description='测试报告',
#     )
#     runner.run(suite)