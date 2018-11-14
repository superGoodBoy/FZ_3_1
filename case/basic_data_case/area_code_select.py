#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren

import unittest,time,re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
"""
1.不选数据直接编辑
2.选择一条直接编辑
"""
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
log=Log()
class Area_code(unittest.TestCase):
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

    def select_areacode(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[45]

        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        time.sleep(3)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        
    def test_query_areacode(self):
        self.select_areacode()
        code = '04'
        self.driver.find_element_by_name("areacode").send_keys(code)
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
        right_up_num_mysql = str(db.select(table="t_areacode", colume='areacode',
                                           condition="areacode like  '%s%%'" % code).__len__())
        log.debug(right_up_num_mysql)
        self.assertEqual(right_up_num_mysql, right_up_num_web)
        content = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content = content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                log.debug("mysql有数据，web页面没有回显")
            else:
                log.debug("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            log.debug("页面无数据")

    def test_query_province(self):

        self.select_areacode()
        code = '河北省'
        self.driver.find_elements_by_tag_name("input")[1].click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div/dl/dd[6]").click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(0.7)
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
        right_up_num_mysql = str(db.select(table="t_areacode", colume='areacode',
                                           condition="provincename='%s'" %code).__len__())
        log.debug("mysql查到的条数: %s" %right_up_num_web)
        self.assertEqual(right_up_num_mysql, right_up_num_web)
        content = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content = content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                log.debug("mysql有数据，web页面没有回显")
            else:
                log.debug("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            log.debug("页面无数据")

    def test_query_city(self):
        driver=self.driver

        self.select_areacode()
        code1 = '江苏省'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(2) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/div/dl/dd[9]").click()

        code2 = '镇江市'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(3) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[4]").click()
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
        right_up_num_mysql = str(db.select(table="t_areacode", colume='areacode',
                                           condition="areaname='%s' and provincename='%s'" %(code2,code1)).__len__())
        log.debug(right_up_num_web)
        self.assertEqual(right_up_num_mysql,right_up_num_web)
        content = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content = content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                log.debug("mysql有数据，web页面没有回显")
            else:
                log.debug("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            log.debug("页面无数据")

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Country_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码添加功能",
#         description='测试报告',
#     )
#     runner.run(suite)