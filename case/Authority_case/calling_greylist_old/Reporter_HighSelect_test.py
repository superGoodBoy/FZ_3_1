# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time
from CINTEL_FZweb3_1_1.tote_box.highselect_getmysql import getmysql
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner

class HighSelect(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=40f8bfa9-9cb3-413f-ae8f-65dd889b67d9")

    def high_select(self,greynumber):
        time.sleep(2)
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.find_element_by_xpath("//div[@id='taskOrder']/div/div/i").click()
        time.sleep(3)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))
        time.sleep(2)
        self.driver.find_element_by_name("calling_number").send_keys(greynumber)

    #--------------输入号码直接查询
    def test_detail_num_select(self):

        greynumber ="86186140689881"
        self.high_select(greynumber)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(2)
        GET_INDEX =(self.driver.find_element_by_class_name("mailbox-controls").text,'utf-8')
        time.sleep(2)
        recever_list = GET_INDEX[0].replace("\\ue605\n" ,"\\n\\ue603").split("\n")
        self.assertEqual(recever_list[14],greynumber)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        #-------------输入时间直接查询
    def test_time_select(self):
        greynumber =""
        self.high_select(greynumber)
        self.driver.find_element_by_xpath("//*[@id='LAY_demorange_se']").click()
        time.sleep(2)
        self.driver.find_element_by_id("layui-laydate1")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='layui-laydate1']/div[1]/div[2]/table/tbody/tr[3]/td[2]").click()
        self.driver.find_element_by_xpath("//*[@id='layui-laydate1']/div[1]/div[2]/table/tbody/tr[3]/td[3]").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]")
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/span[2]").click()
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(6)
        GET_INDEX = (self.driver.find_element_by_class_name("mailbox-controls").text, 'utf-8')
        time.sleep(2)
        recever_list = GET_INDEX[0].replace("\\ue605\n", "\\n\\ue603").split("\n")

        num_list=[]
        num_list.append(recever_list[14])
        num_list.append(recever_list[31])
        num_list.sort()

        mysql_list=getmysql(sql = """
                          SELECT
                              calling_number
                          FROM
                              t_greylist
                          WHERE
                              ca_status = 1
                          and police_status=0
                          AND create_time >= '2018-01-15 00:00:00'
                          AND create_time <= '2018-01-16 00:00:00'
                      """)
        print(mysql_list)
        self.assertListEqual(num_list , mysql_list)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        #-------------输入加灰原因直接查询
    def test_reason_test(self):
        greynumber =""
        self.high_select(greynumber)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[8]/div/div").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[8]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[8]/div/div/dl/dd[31]").click()
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()

        #获取数据库数据list
        mysql_list = getmysql(sql="""
                                    SELECT
                                        calling_number
                                    FROM
                                        t_greylist
                                    WHERE
                                        ca_status = 1
                                    AND (creator_type = 4
                                    OR creator_type = 6)
                                    AND add_reason = 15
                                    AND police_status = 0
                                    AND cm_deliver_status=0
                                    AND cu_deliver_status=0
                                    AND	cr_deliver_status=0
                                    AND	ct_deliver_status=0
                              """)
        # print(mysql_list)
        #获取web数据list
        GET_INDEX = (self.driver.find_element_by_class_name("mailbox-controls").text, 'utf-8')
        time.sleep(2)
        recever_list = GET_INDEX[0].replace("\\ue605\n", "\\n\\ue603").split("\n")
        time.sleep(2)
        web_num=[]
        web_num.append(recever_list[14])
        web_num.append(recever_list[32])
        web_num.append(recever_list[50])
        web_num.append(recever_list[68])
        web_num.append(recever_list[86])
        web_num.append(recever_list[104])
        web_num.sort()
        self.assertEqual(web_num,mysql_list)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

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


if __name__ == 'rqw_HighSelect_test':
    box=unittest.TestSuite()
    box.addTest(HighSelect("test_detail_num_select"))
    box.addTest(HighSelect("test_time_select"))
    box.addTest(HighSelect("test_reason_test"))
    with open('html1.html', 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title='FZweb3_1_UI自动化高级查询测试报告',
            description='用例执行情况'
        )
        runner.run(box)
