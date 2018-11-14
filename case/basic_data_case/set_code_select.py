#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,re
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""

"""
log=Log()

class Set_code(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def select_setcode(self):
        log.info("用户登录输入")
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[47]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_query_operator(self):
        log.info("运营商电信 查询用例开始执行")
        self.select_setcode()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[1]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(1) > div > div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[1]/div/div/dl/dd[4]").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(2)
        right_up_num_str = self.driver.find_element_by_class_name("layui-laypage-count").text

        right_up_num_web = re.findall(r"\d+\.?\d*", right_up_num_str)[0]

        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        right_up_num_mysql = []
        right_up_num_mysql = str(db.select(table="t_setcode", colume='set_code',
                                           condition='set_domain=0').__len__())
        log.debug(right_up_num_mysql)
        self.assertEqual(right_up_num_web, right_up_num_mysql)

    def test_query_nettype(self):
        log.info("网络类型TDM 用例查询开始执行")
        self.select_setcode()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(2) > div > div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div/dl/dd[2]").click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(1)
        right_up_num_str = self.driver.find_element_by_class_name("layui-laypage-count").text
        import re
        right_up_num_web = re.findall(r"\d+\.?\d*", right_up_num_str)[0]

        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        right_up_num_mysql = []
        right_up_num_mysql = str(db.select(table="t_setcode", colume='set_code',
                                           condition='set_networktype=3').__len__())
        log.debug(right_up_num_web)
        self.assertEqual(right_up_num_web, right_up_num_mysql)

    def test_query_setname(self):
        log.info("长途区号名称用例查询开始执行")
        self.select_setcode()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(3) > div > div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[13]").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(2)
        right_up_num_str = self.driver.find_element_by_class_name("layui-laypage-count").text
        right_up_num_web = re.findall(r"\d+\.?\d*", right_up_num_str)[0]

        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        right_up_num_mysql = []
        right_up_num_mysql = str(db.select(table="t_setcode", colume='set_code',
                                           condition='set_name="唐山T局3-2"').__len__())
        log.debug(right_up_num_web)
        self.assertEqual(right_up_num_web, right_up_num_mysql)

if __name__ == '__main__':
    unittest.main()