#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import unittest,time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql

log= Log()
dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
class System_log(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=32f83062-f019-4f1e-92f5-3498ea860ccc")
        self.accept_next_alert = True

    def login(self):
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_id("vcode").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn=self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('czrz')\"]")
        action=ActionChains(self.driver)
        write= self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('czrz')\"]")
        action.move_to_element(write).perform()
        click_btn.click()

        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | index=0 | ]]
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(2)

    def test_query_date(self):
        self.login()
        his='2017-02-23'
        now_time=time.strftime("%Y-%m-%d")
        js='document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 00:00:00"'%(his,now_time)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()

        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-laypage-count"))
        fact_count = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db=Mysql(dbconfig)
        expe_count = db.select(table="t_operatelog",colume="login_name,username",condition="operate_time>='%s' and operate_time<='%s' order by operate_time "%(his,now_time)).__len__()
        db.close()
        self.assertEqual(fact_count,expe_count)

        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | relative=parent | ]]
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_queryUSERname(self):
        self.login()
        username="超级管理员"
        self.driver.find_element_by_name("username").send_keys(username)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        log.debug("判定页面是否有数据,%s"%self.is_element_present(how=By.CLASS_NAME,what='layui-laypage-count'))
        fact_count = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_count = db.select(table="t_operatelog", colume="login_name,username",condition="username='%s' order by operate_time " %username).__len__()
        db.close()
        self.assertEqual(fact_count, expe_count)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_querystatus(self):
        """操作类型"""
        self.login()
        function_id=0
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[2]").click()  #后 2参数为下发
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        log.debug("判定页面是否有数据,%s" % self.is_element_present(how=By.CLASS_NAME, what='layui-laypage-count'))
        fact_count = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_count = db.select(table="t_operatelog", colume="login_name,username",condition="operate_type='%s' order by operate_time " %function_id).__len__()
        db.close()
        self.assertEqual(fact_count, expe_count)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_querytitle(self):
        """功能类型"""
        self.login()
        function_id = 38
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/dl/dd[2]").click()  # 后 2参数为下发
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        log.debug("判定页面是否有数据,%s" % self.is_element_present(how=By.CLASS_NAME, what='layui-laypage-count'))
        fact_count = int(re.findall(r"\d+\.?\d*", self.driver.find_element_by_class_name("layui-laypage-count").text)[0])
        db = Mysql(dbconfig)
        expe_count = db.select(table="t_operatelog", colume="login_name,username",condition="function_id='%s' order by operate_time " % function_id).__len__()
        db.close()
        self.assertEqual(fact_count, expe_count)

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

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
