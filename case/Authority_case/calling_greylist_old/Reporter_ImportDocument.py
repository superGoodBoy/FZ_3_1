# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,xlrd
from CINTEL_FZweb3_1_1.case.tote_box_level01.userdata import *
from CINTEL_FZweb3_1_1.case.tote_box_level01.callExe import callexe
from CINTEL_FZweb3_1_1.case.tote_box_level01.excel_read import readExcel
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
from CINTEL_FZweb3_1_1.tote_box.mysql import mysql_data
"""
        # # 内容用例:
        # 手机号码空验证
        # 加灰原因空验证
        # 内容全部为空验证
        # 某几行或一行某个字段为空验证
        
         u"号码已存在导入验证"
        # ControlSetText("打开","","Edit1","D:\document\灰名单号码模版2018年01月07日21时50分50秒.xlsx")
        # 将excel文档编辑
        # 调用exe文件
        # 灰名单号码模版2017年12月28日13时08分27秒import_templete_existsNum
        # 遍历sheet1中所有行row   num_rows-1 所有记录
        # 拿出一个个号码
        # 使用sql对一个个号码在数据库中查询
        # 查询到拿出该号码并提示已存在
        # 如果找不到则continue

"""
class ImportDocument(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=9f4d1041-3f81-499c-864e-0e6e01841264")
        self.verificationErrors = []
        self.accept_next_alert = True

    def import_Document(self, uname, pwd):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys(uname)
        driver.find_element_by_id("password").send_keys(pwd)
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='taskOrder']/div/div/i").click()
        time.sleep(2)
        driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))

    def test_importDocument_allZero(self):
        u'模板内容全部为空导入验证'
        # ControlSetText("打开","","Edit1","D:\document\灰名单号码模版2018年01月07日21时50分50秒.xlsx")
        uuname = username
        ppwd = password
        self.import_Document(uuname, ppwd)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='importbtn']").click()
        time.sleep(2)
        callexe(self, exe_file="import_Allzero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        time.sleep(3)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"Excel文件中没有任何数据"
        self.assertEqual(fact_result, expect_result)

    def test_importDocument_numZero(self):
        u"导入一条,号码不填,加灰原因填写验证:提示语不友好"
        # ControlSetText("打开","","Edit1","D:\document\灰名单号码模版2018年01月07日21时50分50秒.xlsx")

        uuname = username
        ppwd = password
        self.import_Document(uuname, ppwd)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='importbtn']").click()
        time.sleep(2)
        callexe(self, exe_file="import_templete_numZero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        time.sleep(3)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"成功导入0条记录"
        self.assertEqual(fact_result, expect_result)

    def test_importDocument_reasonZero(self):
        u"导入一条,号码填写,加灰原因不填验证:没有必填验证"
        # ControlSetText("打开","","Edit1","D:\document\灰名单号码模版2018年01月07日21时50分50秒.xlsx")

        uuname = username
        ppwd = password
        self.import_Document(uuname, ppwd)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='importbtn']").click()
        time.sleep(2)
        callexe(self, exe_file="import_reasonZero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        time.sleep(3)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"成功导入0条记录"
        self.assertEqual(fact_result, expect_result)

    def test_importDocument_existsNum(self):
        u"号码已存在导入验证"
        uuname = username
        ppwd = password
        self.import_Document(uuname, ppwd)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='importbtn']").click()
        time.sleep(3)
        callexe(self, exe_file="import_existsNum.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        time.sleep(3)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        list =[]
        workbook = xlrd.open_workbook(r"C:\Users\renqiwei\Desktop\study\import_test\灰名单号码模版2017年12月28日13时08分27秒.xlsx")
        worksheets = workbook.sheet_names()
        # print('worksheets is %s' % worksheets)
        worksheet1 = workbook.sheet_by_name(u'灰名单号码')
        for worksheet_name in worksheets:
            worksheet = workbook.sheet_by_name(worksheet_name)
        # print(worksheet)
        num_rows = worksheet1.nrows
        for curr_row in range(num_rows):
            if curr_row > 0:
                row = worksheet1.row_values(curr_row)
                print(row[0] ,row[1])
                greynum =row[0]
                test_num=mysql_data(self,num=greynum)
                print(test_num,greynum)
                print(type(greynum),type(test_num))
                if test_num == greynum:
                    print("已存在",test_num)
                    list.append(test_num)
                else:
                    print("库中不含有，已添加")
        expect_result = u"成功导入0条记录\n以下主叫号码数据库中已经存在:\n %s\n" %list
        print(expect_result)
        self.assertEqual(fact_result, expect_result)

    def test_other_file(self):
        u"导入.png的文件提示"
        # ControlSetText("打开","","Edit1","D:\document\灰名单号码模版2018年01月07日21时50分50秒.xlsx")
        uuname = username
        ppwd = password
        self.import_Document(uuname, ppwd)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='importbtn']").click()
        time.sleep(3)
        callexe(self, exe_file="import_other_file.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        time.sleep(3)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        print(fact_result)
        excpect_result ="请使用Excel2007及以上版本，后缀名为.xlsx"
        self.assertEqual(fact_result,excpect_result)


    def test_expeort_all(self):
        u"批量导入test"
        # ControlSetText("打开","","Edit1","D:\document\灰名单号码模版2018年01月07日21时50分50秒.xlsx")
        uuname = username
        ppwd = password
        self.import_Document(uuname, ppwd)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='importbtn']").click()
        time.sleep(3)
        callexe(self, exe_file="import_expeort_all.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        time.sleep(3)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        print(fact_result)
        excpect_result = "成功导入100条记录"
        self.assertEqual(fact_result, excpect_result)

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
    box.addTest(ImportDocument("test_importDocument_allZero"))
    box.addTest(ImportDocument("test_importDocument_reasonZero"))
    box.addTest(ImportDocument("test_importDocument_existsNum"))
    box.addTest(ImportDocument("test_other_file"))
    box.addTest(ImportDocument("test_expeort_all"))

    with open("ExportDocument.html", "wb") as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title=u"FZweb3_1灰名单录入importDocument功能测试",
            description=u"测试报告",
            # tester="QIWEI.REN"
        )
        runner.run(box)
        f.close()