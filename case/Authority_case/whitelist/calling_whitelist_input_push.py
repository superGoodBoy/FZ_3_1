# -*- coding: utf-8 -*-
import unittest, time
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import Log
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql
from selenium.webdriver.support.ui import WebDriverWait
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner

log=Log()
class Push(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ct_operator")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        driver.find_element_by_css_selector("div.login-btn").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_css_selector("#taskOrder > div:nth-child(4) > div > span").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_xpath(".//iframe"))

    def test_nochoice_alreadypush(self):
        u"已推送不选择直接点击推送按钮"
        driver=self.driver
        self.login()
        time.sleep(2)

        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        WebDriverWait(driver,10).until(lambda driver:driver.find_element_by_class_name("layui-layer-content").text)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expect_name="请在待推送页面进行推送操作！"
        self.assertEqual(expect_name,fact_name)

    def test_select_alreadypush(self):
        u"已推送选择三条数据点击推送按钮"
        driver =self.driver
        self.login()
        time.sleep(2)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()

        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div/i").click()
        driver.find_element_by_xpath( "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[1]/div/div/i").click()
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[4]/td[1]/div/div/i").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-content").text)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "请在待推送页面进行推送操作！"
        self.assertEqual(expect_name, fact_name)

    #待推送 选择按钮yes or no
    def test_nochoice_push(self):
        u"待推送不选择直接点击推送按钮"
        driver=self.driver
        self.login()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("layui-layer-content").text)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name= "请选择要推送的行"
        self.assertEqual(fact_name,expect_name)

    def test_selectbox_push(self):
        u"待推送校验成功提示语，ca_status，匹配推送号码,"
        driver = self.driver

        self.login()
        time.sleep(3)
        # driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[2]/td/div/div/i").click()
        # driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[4]/td/div/div/i").click()
        # driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[3]/td/div/div/i").click()
        driver.find_element_by_css_selector("body>div.box.box-primary>div.box-body>div>div>div>div>div.layui-table-fixed.layui-table-fixed-l>div.layui-table-body>table>tbody>tr:nth-child(2)>td:nth-child(1)>div").click()
        driver.find_element_by_css_selector("body>div.box.box-primary>div.box-body>div>div>div>div>div.layui-table-fixed.layui-table-fixed-l>div.layui-table-body>table>tbody>tr:nth-child(3)>td:nth-child(1)>div").click()
        driver.find_element_by_css_selector("body>div.box.box-primary>div.box-body>div>div>div>div>div.layui-table-fixed.layui-table-fixed-l>div.layui-table-body>table>tbody>tr:nth-child(4)>td:nth-child(1)>div").click()
        enum1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[2]/div").text
        enum2 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/div").text
        enum3 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[4]/td[2]/div").text
        dbconfig = {
            'db': 'rg_web3_1',
            'host': '192.168.2.87',
            'port': 3306,
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(dbconfig)
        status_his_enum1 =db.select(table='t_whitelist', colume='calling_number,ca_status', condition='calling_number=%s' % enum1)[0]
        status_his_enum2 =db.select(table='t_whitelist', colume='calling_number,ca_status', condition='calling_number=%s' % enum2)[0]
        status_his_enum3 =db.select(table='t_whitelist', colume='calling_number,ca_status', condition='calling_number=%s' % enum3)[0]
        db.close()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()

        driver.find_element_by_link_text(u"确定").click()

        fact_name = driver.find_element_by_xpath("/html/body/div[3]/div").text
        expect_name = "推送成功"
        self.assertEqual(fact_name, expect_name)
        fact_num = []
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        # time.sleep(30)
        num1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[2]/div").text
        num2 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[2]/div").text
        num3 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/div").text
        dbconfig = {
            'db': 'rg_web3_1',
            'host': '192.168.2.87',
            'port': 3306,
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(dbconfig)
        status_now_num1 = db.select(table='t_whitelist', colume='calling_number,ca_status', condition='calling_number=%s' % num1)[0]
        status_now_num2 = db.select(table='t_whitelist', colume='calling_number,ca_status', condition='calling_number=%s' % num2)[0]
        status_now_num3 = db.select(table='t_whitelist', colume='calling_number,ca_status', condition='calling_number=%s' % num3)[0]
        db.close()
        fact_num.append(status_now_num1),fact_num.append(status_now_num2),fact_num.append(status_now_num3)
        fact_num.append(status_his_enum1),fact_num.append(status_his_enum2),fact_num.append(status_his_enum3)
        log.debug("推送前后对比:%s" %fact_num)
        self.assertNotEqual(status_now_num1,status_his_enum1)
        self.assertNotEqual(status_now_num2,status_his_enum2)
        self.assertNotEqual(status_now_num1,status_his_enum3)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()