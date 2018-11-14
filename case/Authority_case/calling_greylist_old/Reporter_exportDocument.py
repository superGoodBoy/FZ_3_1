#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 15:34
# @Author  : QiWei.Ren
# @Site    : 
# @File    : Reporter_exportDocument.py
# @Software: PyCharm
import unittest
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import xlrd
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
from CINTEL_FZWEB3_1_2_1.case.tote_box_level01.getfile_data_time import *
from CINTEL_FZWEB3_1_2_1.case.tote_box_level01.getfile_num import *
"""
  11121232
    # .在selenium启动浏览器前，为其配置好默认下载文件夹
    # 1.如果需要精确匹配文件名还存在以下问题①匹配文件名是否能够及时同步②文件名在时间转换时发生error
    # ----------精确匹配带有时间的文件名称,因异地服务器跟本机时间和time.sleep的影响无法测算他的名称是否带有乱码
    # 2.下载后是否有成功提示语
  # 4.如果需要判断Excel内容，则需要能够处理Excel的架包以及用自己合适的方法去匹配Excel里的内容。
    # ---①校验加灰原因是否完美导出
    # ②校验导出的加灰号码是否完美导出
    # ---注意事项:该路径下必须存放规格相同的导出的数据文档,不可以存放模板类等不规格的文件

"""

class ExportDocument(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"username": "ct_operator", "passworddd": "123456"}
        ]
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=9c8fc783-c622-4314-ad07-82a5eeb3cd72")
        self.verificationErrors = []
        self.accept_next_alert = True

    def export_Document(self, username, passwd):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys(username)
        driver.find_element_by_id("password").send_keys(passwd)
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='taskOrder']/div/div/i").click()
        time.sleep(3)
        driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))


    def test_file_marked_words(self):
        u"检查下载模板成功提示语,"
        # 下载前文件数量 ,会默认读取C:\Windows\System32下的desktop.ini文件,需要将数量减一
        # #下载路径C:\Users\renqiwei\Downloads
        driver = self.driver
        data_0 = self.data[0]
        username = data_0['username']
        passwod = data_0['passworddd']
        self.export_Document(username, passwod)
        driver.find_element_by_id("exportbtn").click()
        time.sleep(3)
        fact_result = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_result)
        time.sleep(2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = "导出灰名单成功"
        self.assertEqual(fact_result, expect_result)

    def test_file_ornot_exists(self):
        u'检查是否有该文件'
        path_filenum_history = nu(self, num=0) - 1
        print(path_filenum_history, 1)

        driver = self.driver
        data_0 = self.data[0]
        username = data_0['username']
        passwod = data_0['passworddd']
        self.export_Document(username, passwod)
        driver.find_element_by_id("exportbtn").click()

        time.sleep(10)
        # 当前文件数量
        path_filenum_now = nu(self, num=0) - 1
        print(path_filenum_now, 2)
        self.assertNotEqual(path_filenum_history, path_filenum_now)
        time.sleep(2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        self.assertNotEqual(path_filenum_history, path_filenum_now)


    def test_readExcel(self):
        driver = self.driver
        data_0 = self.data[0]
        username = data_0['username']
        passwod = data_0['passworddd']
        self.export_Document(username, passwod)
        driver.find_element_by_id("exportbtn").click()
        time.sleep(2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        time.sleep(5)
        filename = filedata_time_new(self, num=0)
        print(filename)

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
                    # print (table.row_values(i)) # 取前所有列
                    if table.row_values(i)[3] == "":
                        u" 导出的数据加灰原因不能为空"
                        print("导出的数据加灰原因不能为空")
                        self.assertNotEqual(table.row_values(i)[3], "")
                    else:
                        print(table.row_values(i))
                        continue


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    box = unittest.TestSuite()
    box.addTest(ExportDocument("test_file_marked_words"))
    box.addTest(ExportDocument("test_file_ornot_exists"))
    box.addTest(ExportDocument("test_readExcel"))

    with open("ExportDocument.html", "wb") as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title=u"FZweb3_1灰名单录入ExportDocument功能测试",
            description=u"测试报告",
            # tester="QIWEI.REN"
        )
        runner.run(box)
        f.close()