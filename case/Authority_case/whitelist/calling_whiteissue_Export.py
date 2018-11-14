#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# @Site    : 
# @File    : calling_whiteissue_add.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest, time, re,time,xlrd
from CINTEL_FZWEB3_1_2_1.logger.log import *
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *

log=Log()
class Exportwhite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def export_white(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ca_operator")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("vcode").send_keys("8888")
        driver.find_element_by_css_selector("div.login-btn").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_xpath("//div[@id='taskOrder']/div[4]/div/i").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))
        time.sleep(2)

    def test_exportdocument(self):
        u"检查下载文档成功提示语,"
        # 下载前文件数量 ,会默认读取C:\Windows\System32下的desktop.ini文件,需要将数量减一
        driver = self.driver
        path_filenum_history = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads") - 1
        log.debug(path_filenum_history)
        self.export_white()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[4]").click()
        time.sleep(2)
        fact_result = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_result)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = "导出主叫白名单成功"
        self.assertEqual(fact_result, expect_result)
        path_filenum_now = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads")-1
        log.debug(path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)

        filename = filedata_time_level01(name_title="主叫白名单号码-待审核", title_len=36, path=r"C:\Users\renqiwei\Downloads")
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]
        nrows = table.nrows
        log.debug(nrows - 1)
        for i in range(nrows):
            if i > 0:
                if table.row_values(i)[0] == "":
                    u"导出的数据加白号码不能为空"
                    log.debug("导出的数据加白号码不能为空")
                    self.assertNotEqual(table.row_values(i)[0], "")
                else:
                    # log.debug (table.row_values(i)) # 取前所有列
                    if table.row_values(i)[3] == "":
                        u" 导出的数据加白原因不能为空"
                        log.debug("导出的数据加白原因不能为空")
                        self.assertNotEqual(table.row_values(i)[3], "")
                    else:
                        log.debug(table.row_values(i))
                        continue

    def test_exporttemplete(self):
        u"检查下载moban 成功提示语,"
        #下载前文件数量 ,会默认读取C:\Windows\System32下的desktop.ini文件,需要将数量减一  #下载路径C:\Users\renqiwei\Downloads
        driver= self.driver
        self.export_white()
        path_filenum_history = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads") - 1
        log.debug(path_filenum_history)
        time.sleep(10)
        driver.find_element_by_xpath(u"/html/body/div[1]/div[1]/div[1]/div/button[5]").click()
        time.sleep(2)
        fact_result=driver.find_element_by_xpath("/html/body/div[2]/div").text
        log.debug(fact_result)
        time.sleep(2)
        expect_result="导出模板成功"
        self.assertEqual(fact_result,expect_result)
        path_filenum_now = nu(self, num=0,path=r"C:\Users\renqiwei\Downloads")-1
        log.debug(path_filenum_now)
        self.assertNotEqual(path_filenum_history, path_filenum_now)

        filename = filedata_time_level01(name_title="主叫白名单号码模版20", title_len=34, path=r"C:\Users\renqiwei\Downloads")
        log.debug(filename)

        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" % filename)
        sheet1 = data.sheet_by_index(0)
        row_data_0 = sheet1.row_values(0)
        row_data = row_data_0[0]
        log.debug(row_data)
        row_data_expect1 = "主叫号码"
        assert row_data, row_data_expect1
        self.assertEqual(row_data, row_data_expect1)
        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" % filename)
        sheet1 = data.sheet_by_index(0)
        row_data = sheet1.row_values(0)
        log.debug(row_data[1])
        row_data_expect2 = "加白原因"
        self.assertEqual(row_data[1], row_data_expect2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

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
