#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/10 11:59
# @Author  : Qiwei.Ren
# @Site    : 
# @File    : UserLogin.py
# @Software: PyCharm
# encoding: utf-8
# from CINTEL_FZWEB3_1_2_1.tote_box.grid_module import grid_3
import unittest,time
from selenium import webdriver
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
运营商登录测试用例

"""
log=Log()
class Logintest(unittest.TestCase):
        def setUp(self):
                # for host, browser in grid_3().items():
                #         driver = webdriver.Remote(
                #                 command_executor=host,
                #                 desired_capabilities={
                #                         'platform': 'LINUX',
                #                         'browserName': browser,
                #                         'version': '',
                #                         'javascriptEnabled': True
                #                 }
                #         )
                self.data =[
                        {"username":"","password":""},                                                              #用户名非空校验提示
                        {"username":"ct_operator","password":""},                                                 # 密码非空校验提示
                        {"username":"ct_operato232r","password":"123456"},                                       #输入未知账户提示
                        {"username":"ct_operator","password":"33333"},                                           #错误密码校验提示
                        {"username":"CT_OPERATOR","password":"123456"},                                          #用户名区分大小写测试
                        {"username":"itim","password":"ITIM204"},                                                  #密码区分大小写测试
                        {"username":"ct_operator","password":"123456"},                                          #正确登陆校验
                ]
                # self.driver =driver
                self.driver= webdriver.Chrome()
                log.info("打开浏览器")
                self.driver.maximize_window()
                self.driver.implicitly_wait(30)
                url = "http://192.168.2.86:8087/rg_web"
                self.driver.get(url)

        def tearDown(self):
                log.info("关闭浏览器")
                self.driver.close()

        def login(self,username,pwd):
                self.driver.find_element_by_id("login_name").send_keys(username)
                self.driver.find_element_by_id("password").send_keys(pwd)
                self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
                self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()

        def loginsuccess_method(self):
                u'''判断是否获取到登录账户名称'''
                try:
                    text = self.driver.find_element_by_id("person").text
                    print (text)
                    return True
                except Exception as e:
                    print("================")
                    print(e)
                    return False

        def test_user_empty(self):
                u"username,password输入为空判断请输入密码"
                data_1 = self.data[0]
                username = data_1["username"]
                pwd = data_1["password"]
                self.login(username,pwd)
                time.sleep(5)
                fact_result=self.driver.switch_to_alert().text
                except_result ="请输入用户名"
                self.assertEqual( fact_result,except_result)

        def test_pwd_empty(self):
                u"密码输入为空"
                data_1 = self.data[1]
                username = data_1["username"]
                password = data_1["password"]
                self.login(username,password)
                time.sleep(5)
                fact_result=self.driver.switch_to_alert().text
                except_result ="请输入密码"
                self.assertEqual( fact_result,except_result)

        def test_user_zero(self):
                u"未知账户"
                data_1 = self.data[2]
                username = data_1["username"]
                pwd = data_1["password"]
                self.login(username,pwd)
                time.sleep(5)
                fact_result=self.driver.switch_to_alert().text
                except_result ="未知账户"
                self.assertEqual( fact_result,except_result)

        def test_login_error(self):
                u"密码输入错误"
                data_1 = self.data[3]
                username = data_1["username"]
                password = data_1["password"]
                self.login(username,password)
                time.sleep(5)
                fact_result=self.driver.switch_to_alert().text
                except_result ="密码不正确"
                self.assertEqual( fact_result,except_result)

        def test_login_USER(self):
                u"用户名为小写,实际输入大写测试,密码不改动是否能够登陆"
                data_1 = self.data[4]
                username = data_1["username"]
                password = data_1["password"]
                self.login(username,password)
                time.sleep(5)
                fact_result=self.driver.switch_to_alert().text
                except_result ="未知账户"
                self.assertEqual( fact_result,except_result)

        def test_login_PWD(self):
                u"用户名不改动,密码小写,大写测试是否能够登陆"
                data_1 = self.data[5]
                username = data_1["username"]
                password = data_1["password"]
                time.sleep(2)
                self.login(username,password)
                time.sleep(5)
                fact_result=self.driver.switch_to_alert().text
                except_result ="密码不正确"
                self.assertEqual( fact_result,except_result)

        def test_loging_success(self):
                u"用户密码输入正确,登陆成功"
                data_1 = self.data[6]
                username = data_1["username"]
                time.sleep(2)
                password = data_1["password"]
                time.sleep(3)
                self.login(username,password)
                result = self.loginsuccess_method()
                self.assertTrue(result)

# '''
# 调试部分
# '''
# if __name__ == 'Reporter_UserLogin':
#         box=unittest.TestSuite()
#         box.addTest(Logintest("test_user_empty"))
#         box.addTest(Logintest("test_pwd_empty"))
#         box.addTest(Logintest("test_user_zero"))
#         box.addTest(Logintest("test_login_error"))
#         box.addTest(Logintest("test_login_PWD"))
#         box.addTest(Logintest("test_login_PWD"))
#         box.addTest(Logintest("test_loging_success"))
#
#         with open("FZ_login_CN.html","wb") as f:
#                 runner =HTMLTestRunner.HTMLTestRunner(
#                     stream = f,
#                     title = "FZweb3_1登陆测试",
#                     description = "测试报告"
#                 )
#                 runner.run(box)
