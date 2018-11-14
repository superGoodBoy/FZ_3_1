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
 VLRGT码 查询
"""
log=Log()
class Vlrgt_code(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("vlrgt码：结束测试")
        self.driver.close()

    def select_vlgrt(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[48]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_query_date(self):
        """日期范围查询条数"""
        self.select_vlgrt()
        date_his = '2017-05-11'
        date_now = time.strftime('%Y-%m-%d')

        js = "document.getElementById('LAY_demorange_se').value='%s 00:00:00 - %s 00:00:00'" % (date_his, date_now)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()

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
        right_up_num_mysql = str(db.select(table="t_vlrnumber", colume='vlr_number',
                          condition='create_time>="%s 00:00:00" and create_time<="%s 00:00:00"' % (
                          date_his, date_now)).__len__())
        self.assertEqual(right_up_num_mysql, right_up_num_web)
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

    def test_query_vlrnum(self):
        """vlrgt码查询"""
        self.select_vlgrt()
        vlr_number="0838"
        self.driver.find_element_by_name("vlr_number").send_keys(vlr_number)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
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
        right_up_num_mysql = str(db.select(table="t_vlrnumber", colume='vlr_number',
                          condition='vlr_number="%s"' %vlr_number).__len__())
        self.assertEqual(right_up_num_mysql, right_up_num_web)

    def test_query_areacode(self):
        """长途区号查询"""
        self.select_vlgrt()
        area_code = "010"
        self.driver.find_element_by_name("area_code").send_keys(area_code)
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
        right_up_num_mysql = str(db.select(table="t_vlrnumber", colume='vlr_number',
                                           condition='area_code="%s"' % area_code).__len__())
        self.assertEqual(right_up_num_mysql, right_up_num_web)

    def test_query_province(self):
        """指定省份查询："""
        self.select_vlgrt()
        code1 = '北京市'
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(4) > div > div")
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/dl/dd[2]").click()

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
        right_up_num_mysql = str(db.select(table="t_vlrnumber", colume='vlr_number',
                                           condition='province_name="%s"' %code1).__len__())
        self.assertEqual(right_up_num_mysql, right_up_num_web)

    def test_query_city(self):
        """指定省份地市查询：存在bug"""
        self.select_vlgrt()
        code1 = '北京市'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(4) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/dl/dd[2]").click()

        code2 = '北京市'
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(5) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]/i").click()
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
        right_up_num_mysql = str(db.select(table="t_vlrnumber", colume='vlr_number',
                                           condition='area_name="%s" and province_name="%s"' %(code2,code1)).__len__())
        self.assertEqual(right_up_num_mysql, right_up_num_web)

    def test_query_domain(self):
        """根据运营商查询"""
        self.select_vlgrt()
        domain=0
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[6]/div/div/div/input").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#conditionForm > div.selectArea > div:nth-child(6) > div > div")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[6]/div/div/dl/dd[2]").click()

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
        right_up_num_mysql = str(db.select(table="t_vlrnumber", colume='vlr_number',
                                           condition='domain="%s"' % domain).__len__())
        print(right_up_num_web,right_up_num_mysql)
        self.assertEqual(right_up_num_mysql, right_up_num_web)

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Vlrgt_code)
#     runner = HTMLTestRunner.HTM北京市LTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码查询功能",
#         description='测试报告',
#     )
#     runner.run(suite)