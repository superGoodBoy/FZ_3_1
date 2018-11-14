# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.logger.log import Log
from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
log=Log()
class HighSelect(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http:\\192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def high_select(self,whitenumber):
        self.driver.find_element_by_id("login_name").send_keys("ct_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#taskOrder > div:nth-child(4) > div > span").click()
        time.sleep(3)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))
        time.sleep(2)
        self.driver.find_element_by_name("calling_number").send_keys(whitenumber)

    def test_detail_num_select(self):
        "号码查询"
        whitenumber ="18511318445"
        self.high_select(whitenumber)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(2)
        GET_INDEX =(self.driver.find_element_by_class_name("mailbox-controls").text,'utf-8')
        time.sleep(2)
        recever_list = GET_INDEX[0].replace("\\ue605\n" ,"\\n\\ue603").split("\n")
        self.assertEqual(recever_list[8],whitenumber)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_time_select(self):
        "时间查询2018-05-07 00:00:00 - 2018-05-11 00:00:00"
        whitenumber =""
        self.high_select(whitenumber)
        time.sleep(5)
        starttime='2018-01-07'
        endtime= time.strftime('%Y-%m-%d')
        js='document.getElementById("LAY_demorange_se").value ="%s 00:00:00 - %s 00:00:00"'%(starttime,endtime)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(3)
        log.info(self.driver.find_element_by_class_name("mailbox-controls").text)
        notpush=int(self.driver.find_element_by_id("totalRecord_not_push").text)
        yetpush=int(self.driver.find_element_by_id("totalRecord_push").text)

        dbconfig={
            'host':'192.168.2.87',
            'port':3306,
            'db':'rg_web3_1',
            'user':'root',
            'passwd':'123456',
            'charset': 'utf8'
        }
        db=Mysql(dbconfig)
        num = db.select(table='t_whitelist', colume='calling_number',
                        condition='list_type=2 and creator_type=0 and ca_status=0 and create_time>="%s 00:00:00" and create_time<="%s 00:00:00"' % (
                        starttime, endtime))
        self.assertEqual(num.__len__(), notpush)

        num1 = db.select(table='t_whitelist', colume='calling_number',
                         condition='list_type=2 and creator_type=0 and ca_status=1 and create_time>="%s 00:00:00" and create_time<="%s 00:00:00"' % (
                         starttime, endtime))
        self.assertEqual(num1.__len__(), yetpush)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
