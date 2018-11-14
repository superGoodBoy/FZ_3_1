# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql
from selenium.webdriver.support.ui import WebDriverWait
"""
待审核：号码查询    已审核：号码查询    已过期：号码查询     已撤销：号码查询
        时间查询             时间查询           时间查询             时间查询
        运营商状态
        num_status 号码电信运营商状态
        
"""
log=Log()
num_status=[0,1,2,3,4,5]
now_time=time.strftime("%Y-%m-%d")
class HighSelect(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/index.shtml")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def high_select(self):
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        self.driver.find_element_by_xpath("//div[@id='taskOrder']/div[4]/div/i").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))

    def test_query_callingnum(self):
        log.info("待审核界面查询")
        self.high_select()
        time.sleep(5)
        whitenumber='18672723333'
        self.driver.find_elements_by_tag_name("input")[1].send_keys("18672723333")
        self.driver.find_element_by_css_selector("#conditionForm>div.layui-btn-group.btnPosition>button:nth-child(1)").click()
        待审核 = int(self.driver.find_element_by_id("totalRecord_not_check").text)
        已审核 = int(self.driver.find_element_by_id("totalRecord_check").text)
        已撤销 = int(self.driver.find_element_by_id("totalRecord_cancel").text)
        已过期 =int(self.driver.find_element_by_id("totalRecord_expire").text)

        dbconfig = {
            'db': 'rg_web3_1',
            'host': '192.168.2.87',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8',
            'port': 3306
        }
        db = Mysql(dbconfig)
        num=db.select(table='t_whitelist',colume='calling_number,ct_deliver_status',condition="calling_number='%s'" %whitenumber)
        log.debug("%s" %num.__len__())
        log.info("待审核页条数%s"%待审核)
        log.info("已审核页条数%s"%已审核)
        log.info("已撤销页条数%s"%已撤销)
        log.info("已过期页条数%s"%已过期)
        self.assertEqual(num.__len__(),待审核)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_date(self):
        self.high_select()
        his_time='2017-05-05'
        js_value = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 00:00:00"'%(his_time,now_time)
        time.sleep(2)
        self.driver.execute_script(js_value)
        self.driver.find_element_by_css_selector("#conditionForm>div.layui-btn-group.btnPosition>button:nth-child(1)").click()
        try:
            待审核 =int(self.driver.find_element_by_id("totalRecord_not_check").text)
            已审核 = int(self.driver.find_element_by_id("totalRecord_check").text)
            已撤销 = int(self.driver.find_element_by_id("totalRecord_cancel").text)
            已过期 = int(self.driver.find_element_by_id("totalRecord_expire").text)
        except NoSuchElementException as e:
            return False

        dbconfig = {
            'db': 'rg_web3_1',
            'host': '192.168.2.87',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8',
            'port': 3306
        }
        db = Mysql(dbconfig)
        num_0 = db.select(table='t_whitelist', colume='calling_number,ct_deliver_status',
                          condition="create_time>='%s 00:00:00' and create_time<='%s 00:00:00' and ct_deliver_status=%s" % (
                              his_time, now_time, num_status[0]))
        num_1 = db.select(table='t_whitelist', colume='calling_number,ct_deliver_status',
                          condition="create_time>='%s 00:00:00' and create_time<='%s 00:00:00' and ct_deliver_status=%s or ct_deliver_status=%s" % (
                          his_time, now_time, num_status[1], num_status[2]))
        num_2 = db.select(table='t_whitelist', colume='calling_number,ct_deliver_status',
                          condition="create_time>='%s 00:00:00' and create_time<='%s 00:00:00' and ct_deliver_status=%s or ct_deliver_status=%s" % (
                          his_time, now_time, num_status[3], num_status[4]))
        num_3 = db.select(table='t_whitelist', colume='calling_number,ct_deliver_status',
                          condition="create_time>='%s 00:00:00' and create_time<='%s 00:00:00' and ct_deliver_status=%s" % (
                              his_time, now_time,num_status[5]))
        log.info("待审核页条数%s,mysql条数%s" %(待审核,num_0.__len__()))
        log.info("已审核页条数%s,mysql条数%s" %(已审核,num_1.__len__()))
        log.info("已撤销页条数%s,mysql条数%s" %(已撤销,num_2.__len__()))
        log.info("已过期页条数%s,mysql条数%s" %(已过期,num_3.__len__()))
        self.assertEqual(num_0.__len__(), 待审核)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_issue_status(self):
        self.high_select()
        time.sleep(5)
        self.driver.find_elements_by_tag_name("input")[3].click()
        self.driver.find_element_by_css_selector("#conditionForm>div.selectArea>div:nth-child(5)>div>div")
        self.driver.find_element_by_css_selector("#conditionForm>div.selectArea>div:nth-child(5)>div>div>dl>dd:nth-child(2)").click()#weixaifa
        self.driver.find_element_by_css_selector("#conditionForm>div.layui-btn-group.btnPosition>button:nth-child(1)").click()
        fact_num=[]
        try:
            fact_num.append(int(self.driver.find_element_by_id("totalRecord_not_check").text))
            fact_num.append(int(self.driver.find_element_by_id("totalRecord_check").text))
            fact_num.append(int(self.driver.find_element_by_id("totalRecord_cancel").text))
            fact_num.append(int(self.driver.find_element_by_id("totalRecord_expire").text))
        except NoSuchElementException as e:
            return False
        dbconfig = {
            'db': 'rg_web3_1',
            'host': '192.168.2.87',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8',
            'port': 3306
        }
        db = Mysql(dbconfig)
        num=[]
        num.append( db.select(table='t_whitelist', colume='ct_deliver_status',condition="list_type =2 and ca_status =0 and ct_deliver_status=0").__len__())
        num.append( db.select(table='t_whitelist', colume='ct_deliver_status',condition="list_type =2 and ca_status =1  and ct_deliver_status=0 and ct_deliver_status=1").__len__())
        num.append( db.select(table='t_whitelist', colume='ct_deliver_status',condition="list_type =2 and ca_status =1 and ct_deliver_status=0 and ct_deliver_status=2").__len__())
        num.append( db.select(table='t_whitelist', colume='ct_deliver_status',condition="list_type =2 and ca_status =1 and ct_deliver_status=0 and ct_deliver_status=4").__len__())
        log.debug("%s" %num)
        self.assertEqual(num, fact_num)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == 'VLRGT_code_del':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Vlrgt_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码导入功能",
#         description='测试报告',
#     )
#     runner.run(suite)
