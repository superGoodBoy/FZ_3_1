#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
不选直接删除
选择单挑删除
选择多条删除
"""
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
log=Log()
class Vlrgt_code(unittest.TestCase):
    def setUp(self):
        print("VLRGT码删除：开始测试")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        print("VLRGT码删除：结束测试")
        self.driver.close()

    def del_t(self):
        driver = self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[48]
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(driver)
        write = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_del_empty(self):
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
        """单个删除"""
        self.del_t()
        driver = self.driver
        time.sleep(3)
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        content_str=driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text.split("创建时间")[1]
        import re
        content_web = re.findall(r"\d+\.?\d*", content_str)[00]

        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        time.sleep(1)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
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
        content_mysql = db.select(table="t_vlrnumber", colume='vlr_number', condition='vlr_number="%s"' %content_web)
        if content_mysql:
            print("vlrgt:",content_web,"删除失败")
        else:
            print("vlrgt:",content_web,"删除成功")
        db.close()
        self.assertNotEqual(content_mysql, content_web)

    def test_del_fivedel(self):
        """多选直接删除"""
        self.del_t()
        driver = self.driver
        for i in range(6):
            if i > 0:
                driver.find_element_by_xpath(
                    "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[%s]/td/div/div/i" % i).click()

        text = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text
        import re
        num = []
        num.append(re.findall(r"\d+\.?\d*", text)[0 * 8])
        num.append(re.findall(r"\d+\.?\d*", text)[1 * 8])
        num.append(re.findall(r"\d+\.?\d*", text)[2 * 8])
        num.append(re.findall(r"\d+\.?\d*", text)[3 * 8])
        num.append(re.findall(r"\d+\.?\d*", text)[4 * 8])
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        time.sleep(1)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(0.5)
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
        fact = db.select(table="t_vlrnumber", colume='vlr_number',
                         condition='vlr_number="%s" or vlr_number="%s" or vlr_number="%s" or vlr_number="%s" or vlr_number="%s"' % (
                             num[0], num[1], num[2], num[3], num[4]))
        if fact:
            print("vlr:", num, "删除失败")
        else:
            print("vlr:", num, "删除成功")
        db.close()

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == 'VLRGT_code_del':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Vlrgt_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2VLRGT码删除功能",
#         description='测试报告',
#     )
#     runner.run(suite)