# -*- coding: utf-8 -*-
import unittest,time,re
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner

# import importlib,sys
# importlib.reload(sys)
# # sys.setdefaultencoding( "utf-8" )
"""
管局 主叫白名单下发推送自动化

1待推送            2已审核            3已撤销             4已过期
删除不选中数据     删除不选中数据     删除不选中数据      删除不选中数一条
删除选中数一条     删除选中数一条     删除选中数一条      删除选中数一条
管局已审核 管局下发单个运营商删除，下发全部运营商删除

"""
log=Log()
class WhitenumDelete(unittest.TestCase):
    def setUp(self):
        log.info("关闭浏览器")
        self.driver =webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def addwhite(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ca_operator")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        driver.find_element_by_css_selector("div.login-btn").click()
        driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_xpath("//div[@id='taskOrder']/div[4]/div/i").click()
        driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))

    def test_del_empty(self):
        self.addwhite()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_result)
        respect_result = u"请选择要删除的行！"
        self.assertEqual(fact_result, respect_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_empty_2(self):
        self.addwhite()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[2]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div/i").click()

        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"请在待审核或已撤销页面进行删除操作！"
        self.assertEqual(fact_result, respect_result)

    def test_del_empty_3(self):
        self.addwhite()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[3]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr").click()

        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"请选择要删除的行！"
        self.assertEqual(fact_result, respect_result)

    def test_del_empty_4(self):
        self.addwhite()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[4]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"请在待审核或已撤销页面进行删除操作！"
        self.assertEqual(fact_result, respect_result)

    def test_del_success(self):
        self.addwhite()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        text=self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text.split("主叫号码")[2]

        num = re.findall(r"\d+\.?\d*", text)[00]
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        self.driver.find_element_by_link_text(u"确定").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        respect_result = u"删除成功"
        self.assertEqual(fact_result,respect_result)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(dbconfig)
        trueorfalse= db.getTrueOrFalse(table="t_whitelist",colume='calling_number',condition='calling_number=%s'%num)
        if trueorfalse:
            log.info("删除成功")
        else:
            log.error("删除失败")

    def test_del_fail_2(self):
        self.addwhite()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[2]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div/i").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        respect_result = u"请在待审核或已撤销页面进行删除操作！"
        self.assertEqual(fact_result, respect_result)

        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_success_3(self):
        self.addwhite()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[3]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/div/div/i").click()

        text = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text.split("主叫号码")[2]
        num = re.findall(r"\d+\.?\d*", text)[00]
        log.debug(num)

        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        self.driver.find_element_by_link_text(u"确定").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        respect_result = u"删除成功"
        self.assertEqual(fact_result, respect_result)

        dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(dbconfig)
        trueorfalse = db.getTrueOrFalse(table="t_whitelist", colume='calling_number',
                                        condition='calling_number=%s' % num)
        if trueorfalse:
            log.info("删除成功")
        else:
            log.error("删除失败")

        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_not_allowed_4(self):
        self.addwhite()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[4]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        log.debug(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"请在待审核或已撤销页面进行删除操作！"
        self.assertEqual(fact_result, respect_result)

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
