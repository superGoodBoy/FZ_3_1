# -*- encoding: utf-8 -*-
import unittest
import time
import xlrd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZweb3_1_1.case.tote_box_level01.getfile_data import *
from CINTEL_FZweb3_1_1.case.tote_box_level01.getfile_num import *
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# python_Cintel.addforFZ_reprort_level04.python2x.import_and_export
# reload(sys)
# sys.setdefaultencoding('utf-8')

class ExportTemplete(unittest.TestCase):

    def setUp(self):
        self.data =[
            {"username":"ct_operator","pwd":"123456"}
        ]
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()


    def export_templete(self,uname,pword):
        driver = self.driver
        driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=9c8fc783-c622-4314-ad07-82a5eeb3cd72")
        driver.find_element_by_id("login_name").send_keys(uname)
        driver.find_element_by_id("password").send_keys(pword)
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='taskOrder']/div/div/i").click()
        time.sleep(2)
        driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))


    def test_file_marked_words(self):
        u"检查下载模板成功提示语,"
        #下载前文件数量 ,会默认读取C:\Windows\System32下的desktop.ini文件,需要将数量减一  #下载路径C:\Users\renqiwei\Downloads
        driver= self.driver
        data_0=self.data[0]
        username = data_0['username']
        passwod = data_0['pwd']
        self.export_templete(username,passwod)
        driver.find_element_by_xpath(u"//button[@onclick=\"window.location.href='/rg_web/greyListControl/execlTemplet.shtml';layer.msg('导出模板成功')\"]").click()
        fact_result=driver.find_element_by_css_selector("html body div#layui-layer1.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg.layui-layer-hui div.layui-layer-content").text
        print(fact_result)
        time.sleep(2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result="导出模板成功"
        self.assertEqual(fact_result,expect_result)

        #3.点击导出后，判断此默认文件夹下是否有这个文件。
    def test_file_ornot_exists(self):
        u'检验当前路径是否有该文件'
        # 默认会读取到系统目录下system32下的desktop.ini文件
        path_filenum_history=nu(self,num=0)-1
        print(path_filenum_history,1)

        driver= self.driver
        data_0=self.data[0]
        username = data_0['username']
        passwod = data_0['pwd']
        self.export_templete(username,passwod)
        driver.find_element_by_xpath(u"//button[@onclick=\"window.location.href='/rg_web/greyListControl/execlTemplet.shtml';layer.msg('导出模板成功')\"]").click()
        time.sleep(10)
        #当前文件数量
        path_filenum_now =nu(self,num=0)-1
        print (path_filenum_now,2)
        self.assertNotEqual(path_filenum_history,path_filenum_now)
        time.sleep(2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        self.assertNotEqual(path_filenum_history,path_filenum_now)

    def test_filetemplate_one(self):
        u'匹配灰名单文档'
        driver= self.driver
        filename_history= filedata(self,num=0)
        print(filename_history)
        print(type(filename_history))

        data_0=self.data[0]
        username= data_0['username']
        pword = data_0['pwd']
        self.export_templete(username,pword)
        driver.find_element_by_xpath(u"//button[@onclick=\"window.location.href='/rg_web/greyListControl/execlTemplet.shtml';layer.msg('导出模板成功')\"]").click()
        time.sleep(5)
        filename_now= filedata(self,num=0)
        print(filename_now)
        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" %filename_now)
        sheet1 = data.sheet_by_index(0)
        # nrows = sheet1.nrows
        # ncols = sheet1.ncols
        # print(nrows,ncols)
        row_data_0 = sheet1.row_values(0)
        row_data = row_data_0[0]
        print(row_data)
        row_data_expect1= "主叫号码"
        assert row_data , row_data_expect1
        self.assertEqual(row_data,row_data_expect1)

        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_filetemplate_two(self):
        u'匹配灰名单表头'
        #1.尝试获取指定文件名称 ,该文件目录下按照时间排序获得该文件
        driver= self.driver
        filename_history= filedata(self,num=0)
        print(filename_history)
        print(type(filename_history))

        data_0=self.data[0]
        username= data_0['username']
        pword = data_0['pwd']
        self.export_templete(username,pword)
        driver.find_element_by_xpath(u"//button[@onclick=\"window.location.href='/rg_web/greyListControl/execlTemplet.shtml';layer.msg('导出模板成功')\"]").click()
        time.sleep(5)
        filename_now= filedata(self,num=0)
        print(filename_now)
        data = xlrd.open_workbook(r"C:\Users\renqiwei\Downloads\%s" %filename_now)
        sheet1 = data.sheet_by_index(0)
        # nrows = sheet1.nrows
        # ncols = sheet1.ncols
        # print(nrows,ncols)
        row_data = sheet1.row_values(0)
        print(row_data[1])
        row_data_expect2 ="加灰原因"
        self.assertEqual(row_data[1],row_data_expect2)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    # 遍历模板是否有除列头外的数据存在,如果有则断言错误
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "Reporter_ExportTemplete":
     box = unittest.TestSuite()
     box.addTest(ExportTemplete("test_file_marked_words"))
     box.addTest(ExportTemplete("test_file_ornot_exists"))
     box.addTest(ExportTemplete("test_filetemplate_one"))
     box.addTest(ExportTemplete("test_filetemplate_two"))
     with open("ExportTemplete.html","wb") as f :
        runner=HTMLTestRunner.HTMLTestRunner (
        stream = f,
        title = u"FZweb3_1灰名单录入ExportTemplate功能测试",
        description = u"测试报告",
        # tester="QIWEI.REN"
        )
        runner.run(box)