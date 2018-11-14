# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
import unittest, time
from CINTEL_FZweb3_1_1.tote_box.getmysql_status import *
from CINTEL_FZweb3_1_1.tote_box.select_realdelete import *
class Push(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def login(self):
        driver = self.driver
        driver.get("http://192.168.2.87:8081/rg_web/login.shtml")
        driver.find_element_by_css_selector("form[name=\"login_form\"] > div").click()
        driver.find_element_by_id("login_name").send_keys("ct_operator")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_css_selector("div.login-btn").click()
        driver.find_element_by_css_selector("i.main-icon.iconfont").click()
        driver.switch_to_frame(driver.find_element_by_xpath(".//iframe"))
    #已推送选择按钮 yes or no
    def test_nochoice_alreadypush(self):
        u"已推送不选择直接点击推送按钮"
        driver=self.driver
        self.login()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()
        driver.find_element_by_xpath("//button[@onclick='pushToPolice()']").click()
        time.sleep(2)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expect_name="请在待推送页面选择要推送的行"
        self.assertEqual(expect_name,fact_name)

    def test_select_alreadypush(self):
        u"已推送选择三条数据点击推送按钮"
        driver =self.driver
        self.login()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()
        driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[2]/td/div/div/i").click()
        driver.find_element_by_xpath( "//div[3]/div[2]/table/tbody/tr[4]/td/div/div/i").click()
        driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[3]/td/div/div/i").click()
        driver.find_element_by_xpath("//button[@onclick='pushToPolice()']").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "请在待推送页面选择要推送的行"
        self.assertEqual(expect_name, fact_name)

    #待推送 选择按钮yes or no
    def test_nochoice_push(self):
        u"待推送不选择直接点击推送按钮"
        driver=self.driver
        self.login()
        time.sleep(3)
        driver.find_element_by_xpath("//button[@onclick='pushToPolice()']").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name= "请选择要推送的行"
        self.assertEqual(fact_name,expect_name)

    def test_selectbox_push(self):
        u"待推送校验成功提示语，ca_status，匹配推送号码,"
        driver = self.driver
        self.login()
        time.sleep(2)
        driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[2]/td/div/div/i").click()
        driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[4]/td/div/div/i").click()
        driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[3]/td/div/div/i").click()
        expect_num=[]
        enum1=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[2]/div").text
        enum2=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/div").text
        enum3=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[4]/td[2]/div").text
        expect_num.append(enum1)
        expect_num.append(enum2)
        expect_num.append(enum3)
        expect_num.sort()
        status_his_enum1 = getmysql("""select ca_status FROM t_greylist where calling_number =%s""" % enum1)
        status_his_enum2 = getmysql(
            """select ca_status FROM t_greylist where calling_number =%s""" % enum2)
        status_his_enum3 = getmysql("""select ca_status FROM t_greylist where calling_number =%s""" % enum3)
        status_his_enum1.append(enum1)
        status_his_enum2.append(enum2)
        status_his_enum3.append(enum3)

        driver.find_element_by_xpath(
            "//button[@onclick='pushToPolice()']"
        ).click()
        time.sleep(2)
        driver.find_element_by_link_text(u"确定").click()
        time.sleep(2)
        fact_name = driver.find_element_by_xpath(
            "//*[@id='layui-layer2']/div"
        ).text
        expect_name = "推送成功"
        driver.find_element_by_xpath( "/html/body/div[1]/div[3]/div/div/ul/li[2]" ).click()
        time.sleep(3)
        fact_num = []
        num1 = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[2]/div").text
        num2 = driver.find_element_by_xpath( "/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[2]/div").text
        num3 = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/div").text
        fact_num.append(num1)
        fact_num.append(num2)
        fact_num.append(num3)
        fact_num.sort()
        status_now_num1 = getmysql("""select ca_status FROM t_greylist where calling_number =%s""" %num1)
        status_now_num2 = getmysql("""select ca_status FROM t_greylist where calling_number =%s"""%num2)
        status_now_num3 = getmysql("""select ca_status FROM t_greylist where calling_number =%s"""%num3)
        status_now_num1.append(num1)
        status_now_num2.append(num2)
        status_now_num3.append(num3)
        self.assertEqual(fact_name,expect_name)
        self.assertEqual(fact_num,expect_num)
        self.assertNotEqual(status_now_num1,status_his_enum1)
        self.assertNotEqual(status_now_num2,status_his_enum2)
        self.assertNotEqual(status_now_num3,status_his_enum3)
        print(
            "提示语：",fact_name,expect_name,
            "待推送推送成功是否进入以推送：",fact_num,expect_num,
            "待推送推送后数据库status是否转为1：",status_now_num1,
            status_his_enum1,status_now_num2,status_his_enum2,
            status_now_num3,status_his_enum3
        )
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        driver.close()

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
        self.assertEqual([], self.verificationErrors)


# if __name__ == 'greylist_push':
#     box = unittest.TestSuite()
#     box.addTest(Push("test_nochoice_alreadypush"))
#     box.addTest(Push("test_nochoice_push"))
#     box.addTest(Push("test_select_alreadypush"))
#     box.addTest(Push("test_selectbox_push"))
#     with open('push.html','wb') as f:
#         runner =HTMLTestRunner.HTMLTestRunner(
#             stream=f,
#             title='灰名单录入推送测试',
#             description='测试报告',
#             tester='QiWei.Ren'
#         )
#         runner.run(box)
