# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,xlrd
from CINTEL_FZWEB3_1_2_1.logger.log import Log
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import callexe

"""
改-----------------------下发
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
log= Log()
class ImportDocument(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        url='http://192.168.2.87:8080/rg_web/index.shtml'
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def import_Document(self,):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ca_operator")
        driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()

        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_xpath("//div[@id='taskOrder']/div[4]/div/i").click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))
        time.sleep(2)

    def test_importDocument_allZero(self):
        u'模板内容全部为空导入验证:主叫白名单号码模版2018年02月06日14时30分16秒'
        self.import_Document()

        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_Allzero_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content").text)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_result)
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
        u"导入一条,号码不填,加灰原因填写验证:提示语不友好:主叫白名单号码模版2018年02月06日14时34分03秒"
        self.import_Document()

        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_templete_numZero_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content").text)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_result)
        expect_result = u"成功导入0条记录\nexcel中1条记录主叫号码不存在"
        self.assertEqual(fact_result, expect_result)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()


    def test_importDocument_reasonZero(self):
        u"导入一条,号码填写,加灰原因不填验证:没有必填验证:主叫白名单号码模版2018年02月06日14时48分48秒"
        self.import_Document()

        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_reasonZero_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content").text)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_result)
        expect_result = u"成功导入0条记录\n以下为excel中不符合规范的主叫白名单(未导入):\n1863223222:加白原因不能为空"
        self.assertEqual(fact_result, expect_result)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_importDocument_existsNum(self):
        u"号码已存在导入验证:主叫白名单号码模版2018年02月06日14时48分49秒"
        self.import_Document()

        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_existsNum_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content").text)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        expect_result = u"成功导入0条记录\n以下主叫号码数据库中已经存在:\n010243122642"
        log.debug(fact_result)
        self.assertEqual(fact_result, expect_result)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        # workbook = xlrd.open_workbook(r"C:\Users\renqiwei\Desktop\study\import_test\灰名单号码模版2017年12月28日13时08分27秒.xlsx")

    def test_other_file(self):
        u"导入.png的文件提示"

        self.import_Document()

        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_other_file.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content").text)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        log.debug(fact_result)
        excpect_result ="请使用Excel2007及以上版本，后缀名为.xlsx"
        self.assertEqual(fact_result,excpect_result)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_expeort_all(self):
        u"批量导入test:主叫白名单号码模版2018年02月06日14时48分50秒"
        self.import_Document()

        self.driver.find_element_by_xpath("//button[@onclick='batchImport(this)']").click()
        time.sleep(2)
        callexe(exe_file="import_expeort_all_calling_whiteinput.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile")
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content").text)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        log.debug(fact_result)
        excpect_result = "成功导入100条记录"
        self.assertEqual(fact_result, excpect_result)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
#
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
