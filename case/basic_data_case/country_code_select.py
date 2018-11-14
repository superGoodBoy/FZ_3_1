#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,re
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
查询：筛选过滤条件
      增加右上角数据条数是否匹配数据用例
待审核，已审核，已撤销
1匹配条数
2.
"""
log=Log()
class Country_code(unittest.TestCase):
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

    def query_countrycode(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[44]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_querystatus_0(self):
        self.query_countrycode()
        time.sleep(2)
        right_up_num_str=self.driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div").text
        right_up_num_web=re.findall(r"\d+\.?\d*",right_up_num_str)
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
        right_up_num_mysql.append(str(db.select(table="t_countrycode", colume='country_code', condition='cr_deliver_status = 0').__len__()))
        right_up_num_mysql.append(str(db.select(table="t_countrycode", colume='country_code', condition='cr_deliver_status=1 or cr_deliver_status=2').__len__()))
        right_up_num_mysql.append(str(db.select(table="t_countrycode", colume='country_code', condition='cr_deliver_status=3 or ct_deliver_status=4 or cr_deliver_status=5 ').__len__()))

        print("web页面条数",right_up_num_web,"mysql统计条数",right_up_num_mysql)
        self.assertEqual(right_up_num_mysql,right_up_num_web)
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

    def test_query_status_0_date(self):
        "时间查询"
        date_his='2015-05-11'
        date_now='2018-05-02'
        self.query_countrycode()
        # js ="document.getElementById('LAY_demorange_se').value='2015-05-11 00:00:00 - 2018-05-02 00:00:00'"
        js ="document.getElementById('LAY_demorange_se').value='%s 00:00:00 - %s 00:00:00'"%(date_his,date_now)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        right_up_num_str = self.driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div").text
        # 正则表达式提取条数
        import re
        b = re.findall(r"\d+\.?\d*", right_up_num_str)[0]

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
        a=str(db.select(table="t_countrycode", colume='country_code', condition='cr_deliver_status = 0 and create_time>="%s 00:00:00" and create_time<="%s 00:00:00"' %(date_his,date_now)).__len__())
        self.assertEqual(a,b)
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

    def test_query_country_code(self):
        self.query_countrycode()
        code ='009'
        self.driver.find_element_by_id("country_code").send_keys(code)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        right_up_num_str = self.driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div").text
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
        right_up_num_mysql = str(db.select(table="t_countrycode", colume='country_code',
                          condition="country_code like  '%s%%'" %code).__len__())
        print(right_up_num_mysql,right_up_num_web)
        self.assertEqual(right_up_num_mysql,right_up_num_web)
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

    def test_query_status_1(self):
        self.query_countrycode()
        name ='未下发'
        self.driver.find_element_by_id("country_name").send_keys(name)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        right_up_num_str = self.driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div").text
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
        right_up_num_mysql = str(db.select(table="t_countrycode", colume='country_code',
                          condition="cr_deliver_status=1").__len__())
        print(right_up_num_mysql,right_up_num_web)
        self.assertEqual(right_up_num_mysql,right_up_num_web)
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

    def test_4(self):
        self.query_countrycode()
        name = '未下发'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
        right_up_num_str = self.driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div").text
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
        right_up_num_mysql = str(db.select(table="t_countrycode", colume='country_code',
                                           condition="cr_deliver_status=0").__len__())
        print(right_up_num_mysql, right_up_num_web)
        self.assertEqual(right_up_num_mysql, right_up_num_web)
        content=self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div").text
        content=content.split("\n").__len__()
        if right_up_num_mysql:
            "mysql 查到数据"
            if content < 11:
                print("mysql有数据，web页面没有回显")
            else:
                print("mysql查到的数据回显web页面正常")
        else:
            "mysql查不到"
            print("页面无数据")

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