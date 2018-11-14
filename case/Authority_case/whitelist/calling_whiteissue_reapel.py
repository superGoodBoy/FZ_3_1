#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
import unittest, time
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.common.mysql import getTrueOrFalse
import pymysql as mdb
def getmysql(sql):
    con = mdb.connect("192.168.2.87", "root", "123456", "rg_web3_1")
    with con:
        cursor = con.cursor()
        cursor.execute(sql)
        num_status_tuple = cursor.fetchall()
    return num_status_tuple
"""
数据制作：①对应处置任务表 状态码改为相应状态码
          ②处置任务表数据对应号码的id 与t_rulepolicylist 表状态一致   
------------撤销
1.待审核 -不点直接撤销
2.yi审核 -不点直接撤销
3.已撤销 -不点直接撤销
4.已过期 -不点直接撤销
5.已审核 - 已撤销  
5_5      - 已撤销
7.已过期 -申请撤销
7_5      - 已撤销
"""
log=Log()
class Reapel(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://192.168.2.87:8080/rg_web")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ca_operator")
        driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        driver.find_element_by_css_selector("div.login-btn").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_xpath("//*[@id='taskOrder']/div[4]/div/i").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_xpath(".//iframe"))

    def test_reapel_empty(self):
        u"dai审核不选择直接点击撤销按钮"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[2]/i").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "请在已审核或者已过期页面选择要撤销的行"
        self.assertEqual(expect_name, fact_name)

    def test_reapel_empty_2(self):
        u"已审核不选择直接点击撤销按钮"
        driver=self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[2]/i").click()
        time.sleep(2)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expect_name="请选择要撤销的行"
        self.assertEqual(expect_name,fact_name)

    def test_reapel_empty_3(self):
        u"已撤销不选择直接点击撤销按钮"
        driver=self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[3]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[2]/i").click()
        time.sleep(2)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expect_name="请在已审核或者已过期页面选择要撤销的行"
        self.assertEqual(expect_name,fact_name)

    def test_reapel_empty_4(self):
        u"已过期不选择直接点击撤销按钮"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[4]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[2]/i").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "请选择要撤销的行"
        self.assertEqual(expect_name, fact_name)

    def test_reapel_2_success(self):
        u"已审核选择某条数点击撤销按钮"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/div/div/i").click()
        content_text = driver.find_element_by_class_name("mailbox-controls").text
        number_text = content_text.split("主叫号码")[2]
        number_text_history = (re.findall(r"\d+\.?\d*", number_text)[00])
        number_status_history = getmysql(sql="""
                                                SELECT
                                                    ct_deliver_status,
                                                    cm_deliver_status,
                                                    cu_deliver_status,
                                                    cr_deliver_status
                                                FROM
                                                    t_whitelist
                                                WHERE
                                                    calling_number = '%s'
                                                """ % number_text_history)
        ct_operator_status = list(number_status_history)[0][0]
        cm_operator_status = list(number_status_history)[0][1]
        cu_operator_status = list(number_status_history)[0][2]
        cr_operator_status = list(number_status_history)[0][3]
        print("撤销前各运营商状态:", ct_operator_status, cm_operator_status, cu_operator_status, cr_operator_status)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[2]/i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()

        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定撤销吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(5)

        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[3]").click()
        content_text = driver.find_element_by_class_name("mailbox-controls").text
        number_text_now = content_text.split("主叫号码")[2]
        number_text_n = re.findall(r"\d+\.?\d*", number_text_now)[00]
        self.assertEqual(number_text_history, number_text_n)

        number_status = getmysql(sql="""
                                        SELECT
                                          	ct_deliver_status,
                                            cm_deliver_status,
                                            cu_deliver_status,
                                            cr_deliver_status
                                        FROM
                                            t_whitelist
                                        WHERE
                                            calling_number = '%s'
                                        """ % number_text_history)
        ct_operator_status_now = list(number_status)[0][0]
        cm_operator_status_now = list(number_status)[0][1]
        cu_operator_status_now = list(number_status)[0][2]
        cr_operator_status_now = list(number_status)[0][3]
        print("撤销后各运营商状态:", number_text_history,ct_operator_status_now, cm_operator_status_now, cu_operator_status_now,
              cr_operator_status_now)

    def test_reapel_4_fail(self):
        u"已过期选择某条数点击撤销按钮"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[4]").click()
        self.driver.implicitly_wait(30)
        driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/div/div/i").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[2]/i").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "没有符合撤销条件的号码，不需要撤销！"
        self.assertEqual(expect_name, fact_name)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

# if __name__ == '__main__':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Issue)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2主叫白名单下发撤销操作",
#         description='测试情况',
#     )
#     runner.run(suite)