#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time,re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
"""
1.待审核    待选直接删除
2.已审核
3.已撤销

4.待审核  选择一条删除
5.
6.

7.待审核   选择多条删除
8.
9.
"""
log = Log()
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

    def del_t(self):
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

    def test_del_status_待审核_empty(self):
        self.del_t()
        driver=self.driver
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name="请选择要删除的行"
        self.assertEqual(fact_name,expect_name)

    def test_del_已审核_empty(self):
        self.del_t()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[2]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()

        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "请在待审核或已撤销页面进行删除操作"
        self.assertEqual(fact_name, expect_name)

    def test_del_已撤销_empty(self):
        self.del_t()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[3]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()

        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "请选择要删除的行"
        self.assertEqual(fact_name, expect_name)

    def test_del_待审核_success(self):
        """"""
        self.del_t()
        driver = self.driver

        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        text=driver.find_element_by_class_name("mailbox-controls").text.split("国家代码")[2]
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "删除成功"
        num = re.findall(r"\d+\.?\d*", text)[00]
        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        fact = db.select(table="t_countrycode", colume='country_code', condition='country_code="%s"' % num)
        if fact:
            print("countrycode:%s".format(fact),"删除失败")
        else:
            print("countrycode:%s".format(fact),"删除成功")
        db.close()
        self.assertEqual(fact_name, expect_name)

    def test_del_已审核_selecttips(self):
        self.del_t()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[2]").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()

        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        time.sleep(1.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "请在待审核或已撤销页面进行删除操作"
        self.assertEqual(fact_name, expect_name)

    def test_del_已撤销_success(self):
        self.del_t()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[3]").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div/i").click()
        text = driver.find_element_by_class_name("mailbox-controls").text.split("国家代码")[2]
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[3]/i").click()
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "删除成功"
        num = re.findall(r"\d+\.?\d*", text)[00]
        Mysql.dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
        db = Mysql(Mysql.dbconfig)
        fact = db.select(table="t_countrycode", colume='country_code', condition='country_code="%s"' % num)
        if fact:
            print("countrycode查询code:",fact,"删除失败")
        else:
            print("countrycode查询code:",fact,"删除成功")
        db.close()

        self.assertEqual(fact_name, expect_name)

    def test_待审核_morelsuccess(self):
        self.del_t()
        driver = self.driver

        time.sleep(2)
        for i in range(6):
            if i > 0:
                driver.find_element_by_xpath(
                    "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[%s]/td/div/div/i" % i).click()
        # driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td/div/div/i").click()
        # driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td/div/div/i").click()
        text = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text
        num = []
        num.append(re.findall(r"\d+\.?\d*", text)[0 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[1 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[2 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[3 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[4 * 16])

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
        fact = db.select(table="t_countrycode", colume='country_code',
                         condition='country_code="%s" or country_code="%s" or country_code="%s" or country_code="%s" or country_code="%s"' % (
                         num[0], num[1], num[2], num[3], num[4]))
        if fact:
            print(fact)
            print("countrycode:", num, "删除失败")
        else:
            print(fact)
            print("countrycode:", num, "删除成功")
        db.close()

    def test_已审核_morelsuccess(self):
        self.del_t()
        driver = self.driver
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/ul/li[3]").click()
        time.sleep(2)
        for i in range(6):
            if i > 0:
                driver.find_element_by_xpath(
                    "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[%s]/td/div/div/i" % i).click()
        # driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td/div/div/i").click()
        # driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td/div/div/i").click()
        text = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div").text
        num = []
        num.append(re.findall(r"\d+\.?\d*", text)[0 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[1 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[2 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[3 * 16])
        num.append(re.findall(r"\d+\.?\d*", text)[4 * 16])

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
        fact = db.select(table="t_countrycode", colume='country_code',
                         condition='country_code="%s" or country_code="%s" or country_code="%s" or country_code="%s" or country_code="%s"' % (
                         num[0], num[1], num[2], num[3], num[4]))
        if fact:
            print(fact)
            print("countrycode:", num, "删除失败")
        else:
            print(fact)
            print("countrycode:", num, "删除成功")
        db.close()

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