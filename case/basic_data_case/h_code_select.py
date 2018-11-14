#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
from selenium import webdriver
import unittest,time,re
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
---first all 对web页面初始化操作
1.对初始化成功后提示语校验
2.对redis数据及 mysql数据库对比
"""
log= Log()
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
class H_code(unittest.TestCase):
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

    def hcode_select(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[46]
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(driver)
        write = self.driver.find_elements_by_class_name("desktop-app")[46]
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(5)

    def test_query_date(self):
        self.hcode_select()
        driver=self.driver
        # "时间查询"
        date_his = '2015-05-11'
        date_now = '2018-05-02'

        js = "document.getElementById('LAY_demorange_se').value='%s 00:00:00 - %s 00:00:00'" % (date_his, date_now)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(3)
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
        right_up_num_mysql = str(db.select(table="t_hcode", colume='hcode',
                          condition='create_time>="%s 00:00:00" and create_time<="%s 00:00:00"' % (
                          date_his, date_now)).__len__())
        print(right_up_num_mysql)
        self.assertEqual(right_up_num_web, right_up_num_mysql)
        content = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content = content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                print("mysql有数据，web页面没有回显")
            else:
                print("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            print("页面无数据")

    def test_query_hcode(self):
        driver=self.driver
        hcode=1718559
        self.hcode_select()
        self.driver.find_element_by_name("h_code").send_keys(hcode)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(3)
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
        right_up_num_mysql = str(db.select(table="t_hcode", colume='hcode',
                                           condition='h_code="%s"' %hcode).__len__())
        print(right_up_num_mysql)
        self.assertEqual(right_up_num_web, right_up_num_mysql)
        content = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content = content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                print("mysql有数据，web页面没有回显")
            else:
                print("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            print("页面无数据")

    def test_query_province(self):
        driver=self.driver
        self.hcode_select()
        code1 = '江苏省'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(3) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[9]").click()

        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        time.sleep(2)

        right_up_num_str = self.driver.find_element_by_class_name("layui-laypage-count").text
        # 正则表达式提取条数
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
        right_up_num_mysql = str(db.select(table="t_hcode", colume='hcode',
                                           condition='hcode_privince="%s"' %(code1)).__len__())
        print(right_up_num_mysql)
        self.assertEqual(right_up_num_web, right_up_num_mysql)
        content = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content = content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                print("mysql有数据，web页面没有回显")
            else:
                print("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            print("页面无数据")

    def test_query_city(self):
        driver=self.driver
        self.hcode_select()
        code1 = '江苏省'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(3) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/div/div/dl/dd[9]").click()

        code2 = '镇江市'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(4) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/dl/dd[4]").click()
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
        right_up_num_mysql = str(db.select(table="t_hcode", colume='hcode',
                                           condition='hcode_city="%s" and hcode_privince="%s"' %(code2,code1)).__len__())
        print(right_up_num_mysql)
        self.assertEqual(right_up_num_web, right_up_num_mysql)

    def test_query_domain(self):
        driver=self.driver
        self.hcode_select()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(5) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[2]").click()
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
        right_up_num_mysql = str(db.select(table="t_hcode", colume='hcode',
                                           condition='domain=0').__len__())
        print(right_up_num_mysql)
        self.assertEqual(right_up_num_web, right_up_num_mysql)

if __name__ == '__main__':
    unittest.main()