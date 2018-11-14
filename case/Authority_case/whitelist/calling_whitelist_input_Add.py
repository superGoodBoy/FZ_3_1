#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 19:57
# @Author  : Qiwei.Ren
# @Site    : 
# @File    : Reporter_BlackNumAdd.py
# @Software: PyCharm

import  time,unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.logger.log import *
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# from CINTEL_FZWEB3_1_2_1.common
#     for host, browser in grid_2().items():
    #         driver = webdriver.Remote(
    #             command_executor=host,
    #             desired_capabilities={
    #                 'platform': 'ANY',
    #                 'browserName': browser,
    #                 'version': '',
    #                 'javascriptEnabled': True
    #             }
    #         )
"""
zhujiaobaimingdan luru tianjia 
"""
log=Log()
class WhiteNumAdd(unittest.TestCase):
    def setUp(self):

        self.data =[
            {"addwhitenum":"","addwhitereason":""},                                                                   #提示请输入手机号0
            {"addwhitenum":"18511318433","addwhitereason":""},                                                      #提示请输入加灰原因1
            {"addwhitenum":"18511318433","addwhitereason":"rqw"},                                                   #验证号码已存在2
            {"addwhitenum":"#@$$$","addwhitereason":"rqw"},                                                          #输入特殊字符,提示请输入1-30手机号码3
            {"addwhitenum":"1862382322","addwhitereason":"#@#4#@#@￥@￥@￥@%#%#￥sfaf#@#4#@#@￥@￥@￥@%#%#￥sfaf%#@#4#@#@￥@￥@￥@%#%#￥sfaf%%"},                        #输入特殊字符 加灰原因4添加失败
            {"addwhitenum":"186238232218623823221862382322186238232218623823221862382322","addwhitereason":"234242"},          #最长手机号码校验5
            {"addwhitenum":"18511318322","addwhitereason":"186238232218623823221862382322186238232218623823221862382322"},    #最长加灰校验6
            {"addwhitenum":"01033435422642","addwhitereason":"rqw"},
        ]
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
        self.driver.maximize_window()
        self.driver.get("http:\\192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def add(self,addwhitenum,addwhitereason):
        self.driver.find_element_by_id("login_name").send_keys("ct_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#taskOrder > div:nth-child(4) > div > span").click()
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        self.driver.find_element_by_xpath("//button[@onclick='addCallingWhiteList()']").click()
        self.driver.find_element_by_xpath("(//input[@name='calling_number'])[2]").send_keys(addwhitenum)
        self.driver.find_element_by_id("calling_reason").send_keys(addwhitereason)
        self.driver.find_element_by_link_text("保存").click()

    def test_addnum_empty(self):
        u"不输入手机号码提示:"
        data_1=self.data[0]
        print(data_1)
        addwhitenum = data_1['addwhitenum']
        addwhitereason = data_1['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_result =self.driver.execute_script("return arguments[0].textContent", demo_div)
        print(fact_result)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"必填项不能为空"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_addreason_empty(self):
        u"不输入加白原因提示"
        data_0=self.data[1]
        print(data_0)
        addwhitenum = data_0['addwhitenum']
        addwhitereason = data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_result =self.driver.execute_script("return arguments[0].textContent", demo_div)
        print(fact_result)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"必填项不能为空"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_addnum_exists(self):
        u"已存在号码测试"
        data_0=self.data[2]
        print(data_0)
        addwhitenum = data_0['addwhitenum']
        addwhitereason = data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        time.sleep(3)
        demo_div = self.driver.find_element_by_class_name("layui-layer-content")
        fact_result =self.driver.execute_script("return arguments[0].textContent",demo_div)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"白名单已经存在此号码:18511318433"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_mustbenum(self):
        u"特殊字符号码提示"
        data_0=self.data[3]
        print(data_0)
        addwhitenum = data_0['addwhitenum']
        addwhitereason = data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        fact_result=self.driver.find_element_by_css_selector("html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        print(fact_result)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"请输入号码1到30位数字"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_china_reason(self):
        u"输入加灰原因超长提示"
        data_0=self.data[4]
        print(data_0)
        time.sleep(3)
        addwhitenum = data_0['addwhitenum']
        addwhitereason = data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        time.sleep(1)
        fact_result=self.driver.find_element_by_css_selector(
            "html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg"
        ).text
        print(fact_result)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"输入原因不能为空且在50字符 以内 ！"
        self.assertEqual(except_result ,fact_result)

    def test_not_toolong_num(self):
        u"加灰号码输入特长 提示"
        data_0=self.data[5]
        print(data_0)
        addwhitenum = data_0['addwhitenum']
        addwhitereason = data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        fact_result=self.driver.find_element_by_css_selector("html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        print(fact_result)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"请输入号码1到30位数字"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_not_toolong_reason(self):
        u"加灰原因输入特长 提示"
        data_0=self.data[6]
        print(data_0)
        addwhitenum = data_0['addwhitenum']
        addwhitereason = data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        time.sleep(1)
        fact_result=self.driver.find_element_by_css_selector("html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        except_result = u"输入原因不能为空且在50字符 以内 ！"
        print(fact_result, except_result)
        self.assertEqual(except_result, fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_addwhitenum_success(self):
        u"验证成功添加用例"
        data_0=self.data[7]
        print(data_0)
        addwhitenum = data_0['addwhitenum']
        addwhitereason =data_0['addwhitereason']
        self.add(addwhitenum,addwhitereason)
        time.sleep(1)
        fact_result=self.driver.find_element_by_xpath("//*[@id='layui-layer2']/div").text
        except_result=u"添加成功"
        print(fact_result, except_result)
        self.assertEqual(except_result,fact_result)

