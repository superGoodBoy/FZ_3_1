#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,re
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.common.action_chains import ActionChains
"""
不选直接删除
选择单挑删除
选择多条删除:多条删除时 因遍历选择则框有时候会报找不到该选框
"""
log= Log()
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
        driver = self.driver
        driver.close()

    def del_t(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[49]

        action=ActionChains(driver)
        write=self.driver.find_elements_by_class_name("desktop-app")[49]
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_del_zerodel(self):
        """不选直接删除"""
        self.del_t()
        driver=self.driver
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name="请选择要删除的行"
        self.assertEqual(fact_name,expect_name)

    def test_del_onedel(self):
        """选中单条删除"""
        self.del_t()
        driver = self.driver
        time.sleep(3)
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        content_str=driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text.split("创建时间")[1]
        content_web = re.findall(r"\d+\.?\d*", content_str)[00]
        # print(content_web)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        time.sleep(1)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print("捕捉删除提示语",fact_name)
        expect_name = "删除成功"
        self.assertEqual(expect_name,fact_name)
        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        content_mysql = db.select(table="t_specnumber", colume='dep_number', condition='dep_number="%s"' %content_web)
        if content_mysql:
            print("mysql-vlrgt:",content_web,"删除失败")
        else:
            print("mysql-vlrgt:",content_web,"删除成功")
        db.close()
        self.assertNotEqual(content_mysql, content_web)

    def test_del_fivedel(self):
        self.del_t()
        driver = self.driver
        for i in range(6):
            if i > 0:
                time.sleep(0.1)
                driver.find_element_by_xpath(
                    "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[%s]/td/div/div/i" %i).click()

        text = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text
        num = []
        num.append(re.findall(r"\d+\.?\d*", text)[0 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[1 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[2 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[3 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[4 * 16])
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        self.driver.implicitly_wait(30)
        # self.driver.find_element_by_class_name("layui-layer-btn0").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write =  self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "删除成功"
        self.assertEqual(fact_name, expect_name)

        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        fact = db.select(table="t_specnumber", colume='dep_number',
                         condition='dep_number="%s" or dep_number="%s" or dep_number="%s" or dep_number="%s" or dep_number="%s"' % (
                             num[0], num[1], num[2], num[3], num[4]))
        if fact:
            print("spec:", num[:5], "删除成功")
        else:
            print("spec:", num[:5], "删除失败")
        db.close()

# if __name__ == '__main__':
#
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Spec_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2特殊短号码删除功能",
#         description='测试报告',
#     )
#     runner.run(suite)