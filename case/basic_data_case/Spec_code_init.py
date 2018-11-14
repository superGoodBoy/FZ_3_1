#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,re,redis
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
"""
特殊短号码：初始化
"""
log=Log()
class Spec_code(unittest.TestCase):
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

    def test_init(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[49]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write= self.driver.find_elements_by_class_name("desktop-app")[49]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.implicitly_wait(30)

        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[7]").click()
        log.info("进入确定初始化弹出框：%s" %driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_class_name(
           "layui-layer-content"))
        time.sleep(1)
        fact_name=self.driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "初始化成功"
        self.assertEqual(fact_name, expect_name)

        r = redis.Redis(host='192.168.2.51', port=7111)
        text_1 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(
            " ")
        r = redis.Redis(host='192.168.2.51', port=7112)
        text_2 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(
            " ")
        r = redis.Redis(host='192.168.2.52', port=7111)
        text_3 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(
            " ")
        r = redis.Redis(host='192.168.2.52', port=7112)
        text_4 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(
            " ")
        text = text_1 + text_2 + text_3 + text_4
        text = sorted(text)
        # log.info("redis同步数据:%s" %text)
        log.info("redis同步数据条数: %s" %text.__len__())

        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        fact = db.select(table="t_specnumber", colume='dep_number')
        sorted(fact)
        # log.info("mysql数据：%s"%fact)
        log.info("mysql数据：%s" %fact.__len__())

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == 'Spec_code_init':
#
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Spec_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2特殊短号码初始化功能",
#         description='测试报告',
#     )
#     runner.run(suite)