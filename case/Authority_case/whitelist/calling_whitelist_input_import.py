# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time, re,xlrd
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *

dbconfig={
    'db':'rg_web3_1',
    'host':'192.168.2.87',
    'port':3306,
    'user':'root',
    'passwd':'123456',
    'charset':'utf8'
}
log=Log()
class ImportDocument(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def import_Document(self):
        self.driver.find_element_by_id("login_name").send_keys("ct_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        self.driver.find_element_by_xpath("//*[@id='taskOrder']/div[4]/div").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))
        self.driver.implicitly_wait(30)

    def test_importDocument_allZero(self):
        u"模板内容全部为空导入验证:主叫白名单号码模版2018年02月06日14时30分16秒"
        self.import_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_Allzero_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        expect_result = u"Excel文件中没有任何数据"
        self.assertEqual(fact_result, expect_result)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_importDocument_numZero(self):
        u"导入一条,号码不填,加白原因填写验证:主叫白名单号码模版2018年02月06日14时34分03秒"
        self.import_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_templete_numZero_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"成功导入0条记录\nexcel中1条记录主叫号码不存在"
        self.assertEqual(fact_result, expect_result)

    def test_importDocument_reasonZero(self):
        u"导入一条,号码填写,加白原因不填验证:主叫白名单号码模版2018年02月06日14时48分48秒"
        self.import_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_reasonZero_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"成功导入0条记录\n以下为excel中不符合规范的主叫白名单(未导入):\n1863223222:加白原因不能为空"
        self.assertEqual(fact_result, expect_result)

    def test_importDocument_existsNum(self):
        u"号码已存在导入验证:主叫白名单号码模版2018年02月06日14时48分49秒"
        self.import_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(3)
        callexe(exe_file="import_existsNum_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        list =[]
        expect_result = u"成功导入0条记录\n以下主叫号码数据库中已经存在:\n010243122642"
        print(expect_result,fact_result)
        self.assertEqual(fact_result, expect_result)

    def test_other_file(self):
        u"导入.png的文件提示"
        self.import_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(3)
        callexe(exe_file="import_other_file.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        print(fact_result)
        excpect_result ="请使用Excel2007及以上版本，后缀名为.xlsx"
        self.assertEqual(fact_result,excpect_result)

    def test_expeort_all(self):
        u"批量导入test：主叫白名单号码模版2018年02月06日14时48分50秒"
        self.import_Document()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(3)
        callexe( exe_file="import_expeort_all_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        print(fact_result)
        excpect_result = "成功导入100条记录"
        self.assertEqual(fact_result, excpect_result)