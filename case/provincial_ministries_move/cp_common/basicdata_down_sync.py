#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
import unittest, time, re
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from CINTEL_FZWEB3_1_2_1.common.mysql import *
"""资源共享类"""

dbconfig = {
    'host': '192.168.2.87',
    'port': 3306,
    'db': 'rg_web3_1',
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8'
}

log= Log()
class Basicdata_down_sync(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml")
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        self.driver.find_element_by_id("login_name").send_keys("ca_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])

        click_btn = self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('zygxl')\"]")
        action = ActionChains(self.driver)
        write = self.driver.find_element_by_xpath("/html/body/div/div[3]/div[1]/div[7]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        for i in range(2):
            time.sleep(1)
            log.info("倒计时%s" % (2 - i))

    def test_queryDATE_cp_share_numquerydown(self):
        """码号下行查询: cp_share_numquerydown（码号下行查询记录表）"""
        self.login()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his="2017-01-03 00:00:00"
        now =time.strftime("%Y-%m-%d")
        js='document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"'%(his,now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db=Mysql(dbconfig)
        expe_name=db.select('cp_share_numquerydown','serial_number','create_time>="%s" and create_time <="%s"'%(his,now)).__len__()
        db.close()
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_numquerydown(self):
        """码号下行查询: cp_share_numquerydown（码号下行查询记录表）"""
        self.login()
        tak="322222"
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numquerydown', 'serial_number','task_id="%s"' % tak).__len__()
        db.close()
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_querySTATUS_cp_share_numquerydown(self):
        """码号下行查询: cp_share_numquerydown（码号下行查询记录表）"""
        self.login()

        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[3]").click()
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numquerydown', 'serial_number',
                              '	result_status=1').__len__()
        db.close()
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(3)
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        import re
        fact_name = int(re.findall(r"\d+\.?\d*",self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numqueryup', 'serial_number',
                              'create_time>="%s" and create_time <="%s"' % (his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak='201806111423270701101457'
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numqueryup', 'serial_number',
                              'task_id="%s"' % (tak)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_querySTATUS_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表） 已发送"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[3]").click()

        self.driver.find_element_by_class_name("layui-icon").click()
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numqueryup', 'serial_number',
                              'result_status=1').__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_addnumempty_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表） 已发送"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[1]").click()
        '''默认值'''

        self.driver.find_element_by_name("number").send_keys("")              #haoma
        # self.driver.find_element_by_xpath("//*[@id='sheng]/div[4]/i").click()  #yunnan　默认值
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_elements_by_class_name("layui-layer-content")[1].text
        expe_name="必填项不能为空"
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_addsuccess_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表） 已发送"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[1]").click()
        '''默认值'''
        # self.driver.find_element_by_xpath("//*[@id='add_tqu_form']/div[1]/div/div/div/input").click()
        # self.driver.find_element_by_xpath("//*[@id='add_tqu_form']/div[1]/div/div")
        # self.driver.implicitly_wait(30)
        # self.driver.find_element_by_xpath("//*[@id='add_tqu_form']/div[1]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_name("number").send_keys("18511318433")              #haoma
        # self.driver.find_element_by_xpath("//*[@id='sheng]/div[4]/i").click()  #yunnan　默认值
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name="添加成功"
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_empty_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表） 已发送"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text
        expe_name="请选择要删除的行"
        self.assertEqual(fact_name,expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_success_cp_share_numqueryup(self):
        """cp_share_numqueryup（码号上行查询记录表） 已发送"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('1')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]").click()
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = self.driver.find_element_by_class_name("layui-layer-content").text

        expe_name = "删除成功"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_templetquerydown(self):
        """cp_share_templetquerydown（模板下行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetquerydown', 'serial_number',
                              'create_time>="%s" and create_time <="%s" group by task_id' % (his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_templetquerydown(self):
        """cp_share_templetquerydown（模板下行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201801020918220601101966"
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetquerydown', 'serial_number', 'task_id="%s" group by task_id' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_querySTATUS_cp_share_templetquerydown(self):
        """cp_share_templetquerydown（模板下行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('4')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[3]").click()

        self.driver.find_element_by_class_name("layui-icon").click()
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetquerydown','serial_number',
                              'back_status=1 group by task_id').__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_templetqureyup(self):
        """cp_share_templetqureyup（模板上行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('3')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()

        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetqueryup', 'serial_number',
                              'create_time>="%s" and create_time <="%s" group by task_id' % (his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_templetqureyup(self):

        """cp_share_templetqureyup（模板上行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('3')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201806111459250701101866"
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetqueryup', 'serial_number',
                              'task_id="%s" group by task_id' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_querySTATUS_cp_share_templetqureyup(self):
        """cp_share_templetqureyup（模板上行查询记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('3')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[3]").click()

        self.driver.find_element_by_class_name("layui-icon").click()
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])

        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetqueryup', 'serial_number',
                              'back_status=1 group by task_id').__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_basicdown(self):
        """cp_share_basicsync基础数据下行同步"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        try:
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as  e:
            print(e)
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_basicsync',
                              'id, serial_number, task_id, sync_type, data_type, status, create_time, resource, update_time',
                              '1 = 1 and resource =1 and create_time >="%s" and create_time <="%s" order by create_time' % (
                              his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_basicdown(self):
        """cp_share_basicsync基础数据down同步"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('6')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201711031419420001045032"
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)

        expe_name = db.select('cp_share_basicsync',
                              'id, serial_number, task_id, sync_type, data_type, status, create_time, resource, update_time',
                              '1 = 1 and resource =1 and task_id="%s" order by create_time' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_basicup(self):
        """cp_share_basicsync基础数据下行同步"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('5')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        try:
            fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as  e:
            print(e)
        db = Mysql(dbconfig)
        expe_name=db.select('cp_share_basicsync',
                           'id, serial_number, task_id, sync_type, data_type, status, create_time, resource, update_time',
                           '1 = 1 and resource =2 and create_time >="%s" and create_time <="%s" order by create_time' % (his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_basicup(self):
        """cp_share_basicsync基础数据up同步"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('5')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201712021457001101031348"
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)

        expe_name = db.select('cp_share_basicsync',
                              'id, serial_number, task_id, sync_type, data_type, status, create_time, resource, update_time',
                              '1 = 1 and resource =2 and task_id="%s" order by create_time' %tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_numsyncdown(self):
        """cp_share_numsync（名单库同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('8')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        try:
            fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as  e:
            print(e)
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numsync',
                              'serial_number',
                              '1 = 1 and resource =1 and create_time >="%s" and create_time <="%s"GROUP BY task_id ORDER BY create_time' % (
                              his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_numsyncdown(self):
        """cp_share_numsync（名单库同步记录表）"""
        try:
            self.login()
            self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('8')\"]").click()
            self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
            tak = "201803161035010001041052"
            self.driver.find_element_by_name("task_id").send_keys(tak)
            self.driver.find_element_by_class_name("layui-icon").click()
            self.driver.implicitly_wait(30)
            WebDriverWait(self.driver,10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
            fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
            db = Mysql(dbconfig)

            expe_name = db.select('cp_share_numsync',
                                  'serial_number',
                                  '1 = 1 and resource =1 and task_id="%s" GROUP BY task_id ORDER BY create_time' % tak).__len__()
            db.close()
            self.assertEqual(fact_name, expe_name)
            self.driver.switch_to_default_content()
            self.driver.switch_to_default_content()
            self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
            self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
            self.driver.find_element_by_xpath("//li[@onclick='quit()']").click(DATE)
        except NoSuchElementException as e:
            print(e)

    def test_queryDATE_cp_share_numsyncup(self):
        """cp_share_numsync（名单库同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('7')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        try:
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as  e:
            print(e)
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_numsync',
                              'serial_number',
                              '1 = 1 and resource =2 and create_time >="%s" and create_time <="%s"GROUP BY task_id ORDER BY create_time' % (
                                  his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_numsyncup(self):
        """cp_share_numsync（名单库同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('7')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201804251701000601031001"
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("task_id"))
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(lambda driver:self.driver.find_element_by_class_name("layui-icon"))
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)

        expe_name = db.select('cp_share_numsync',
                              'serial_number',
                              '1 = 1 and resource =2 and task_id="%s" GROUP BY task_id ORDER BY create_time' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_templetsyncDOWN(self):
        """cp_share_templetsync（YUYIN模板同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('10')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        try:
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as  e:
            print(e)
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetsync',
                              'serial_number',
                              '1 = 1 and resource =1 and create_time >="%s" and create_time <="%s"GROUP BY task_id ORDER BY create_time' % (
                                  his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_templetsyncDOWN(self):
        """cp_share_templetsync（YUYIN模板同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('10')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201711291410001101031545"
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)

        expe_name = db.select('cp_share_templetsync',
                              'serial_number',
                              '1 = 1 and resource =1 and task_id="%s" GROUP BY task_id ORDER BY create_time' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryDATE_cp_share_templetsyncUP(self):
        """cp_share_templetsync（YUYIN模板同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('9')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

        his = "2017-01-03 00:00:00"
        now = time.strftime("%Y-%m-%d")
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s 00:00:00"' % (his, now)
        self.driver.execute_script(js)
        self.driver.find_element_by_class_name("layui-icon").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        try:
            fact_name = int(
                re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        except NoSuchElementException as  e:
            print(e)
        db = Mysql(dbconfig)
        expe_name = db.select('cp_share_templetsync',
                              'serial_number',
                              '1 = 1 and resource =2 and create_time >="%s" and create_time <="%s"GROUP BY task_id ORDER BY create_time' % (
                                  his, now)).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)

        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryTASKID_cp_share_templetsyncUP(self):
        """cp_share_templetsync（YUYIN模板同步记录表）"""
        self.login()
        self.driver.find_element_by_xpath("//li[@onclick=\"loadPage('10')\"]").click()
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        tak = "201711021054010001041040"
        self.driver.find_element_by_name("task_id").send_keys(tak)
        self.driver.find_element_by_class_name("layui-icon").click()
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        fact_name = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)

        expe_name = db.select('cp_share_templetsync',
                              'serial_number',
                              '1 = 1 and resource =1 and task_id="%s" GROUP BY task_id ORDER BY create_time' % tak).__len__()
        db.close()
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

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

if __name__ == "__main__":
    unittest.main()
