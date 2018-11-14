# -*- coding: utf-8 -*-
import unittest, time,re
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import Log
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
"""
运营商 主叫白名单录入删除测试
"""
dbconfig = {
    'db': 'rg_web3_1',
    'host': '192.168.2.87',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8'
}
log=Log()
class WhitenumDelete(unittest.TestCase):
    def setUp(self):
        self.driver =webdriver.Chrome()
        self.driver.maximize_window()
        log.info("打开浏览器")
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def whitenum_delete(self):
        self.driver.find_element_by_id("login_name").send_keys("ct_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        self.driver.find_element_by_css_selector("#taskOrder > div:nth-child(4) > div > span").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        # self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_del_empty_1(self):
        self.whitenum_delete()
        time.sleep(5)
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        print(fact_result)
        respect_result = u"请选择要删除的行"
        self.assertEqual(fact_result, respect_result)

        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_empty_2(self):
        "已推送不选数据直接删除ok"
        self.whitenum_delete()
        time.sleep(5)
        # self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[2]").click()
        self.driver.find_element_by_css_selector("body>div.box.box-primary>div.box-body>div>div>ul>li:nth-child(2)").click()
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result="请选择要删除的行"
        self.assertEqual(fact_result,expect_result)

        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_success_1(self):
        self.whitenum_delete()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div/i").click()
        div = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div").text
        delete_num = div.split('')[3].split('\n')[1]
        print(delete_num)
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        self.driver.find_element_by_link_text(u"确定").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        print(fact_result)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        # time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"删除成功"
        # self.assertEqual(fact_result,respect_result)
        time.sleep(3)
        realDeltrue = getTrueOrFalse("""
                          select calling_number from rg_web3_1.t_whitelist where calling_number=%s
                  """ % delete_num)
        print()
        self.assertTrue(realDeltrue)
        print(fact_result, realDeltrue)

    def test_del_success_2(self):
        u"yi推送删除成功"
        self.whitenum_delete()
        time.sleep(5)
        # self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[2]").click()
        self.driver.find_element_by_css_selector("body>div.box.box-primary>div.box-body>div>div>ul>li:nth-child(2)").click()

        db = Mysql(dbconfig)
        al_num = db.select(table='t_whitelist',colume='calling_number',condition='creator_type=0 AND creator_type=0 AND ca_status=1 and ct_deliver_status=0 AND cr_deliver_status=0 and cm_deliver_status=0 and cu_deliver_status=0 ORDER BY create_time')
        db.close()
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/div/div/i").click()
        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(2)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result="删除成功"

        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        db = Mysql(dbconfig)
        false = db.select(table='t_whitelist',colume='calling_number',condition='calling_number="%s"' %al_num[0])
        db.close()
        self.assertEqual(fact_result, expect_result)
        self.assertFalse(false)
        print(fact_result,false)

    def test_moreDel_1(self):
        self.whitenum_delete()
        time.sleep(4)
        u =[2,3,4]
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div").click()
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[1]/div/div").click()
        time.sleep(2)
        div = self.driver.find_element_by_xpath("/html/body/div").text
        delete_num_0 = div.split('')[2].split('\n')[1]
        delete_num_1= div.split('')[3].split('\n')[1]
        delete_num_2 = div.split('')[4].split('\n')[1]

        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result=self.driver.find_element_by_css_selector(".layui-layer-content").text
        print(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"删除成功"
        realDeltrue = getTrueOrFalse("""
                              SELECT calling_number FROM rg_web3_1.t_whitelist
                                WHERE calling_number = %s
                                OR calling_number = %s
                                OR calling_number = %s
                       """ %(delete_num_0,delete_num_1,delete_num_2))
        log.debug("%s,%s,%s"%(delete_num_0,delete_num_1,delete_num_2))
        self.assertTrue(realDeltrue)
        self.assertEqual(fact_result,respect_result)

    def test_moreDel_2(self):
        self.whitenum_delete()
        time.sleep(4)
        self.driver.find_element_by_css_selector(
            "body>div.box.box-primary>div.box-body>div>div>ul>li:nth-child(2)").click()
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/div/div").click()
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr[3]/td[1]/div/div").click()
        time.sleep(2)
        div = self.driver.find_element_by_xpath("/html/body/div").text
        delete_num_0 = div.split('')[2].split('\n')[1]
        delete_num_1 = div.split('')[3].split('\n')[1]
        delete_num_2 = div.split('')[4].split('\n')[1]

        self.driver.find_element_by_xpath("//button[@onclick='deleteCallingWhiteList()']").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        print(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"删除成功"
        realDeltrue = getTrueOrFalse("""
                                 SELECT
                                       calling_number
                                   FROM
                                       rg_web3_1.t_whitelist
                                   WHERE
                                       calling_number = %s
                                   OR calling_number = %s
                                   OR calling_number = %s
                          """ % (delete_num_0, delete_num_1, delete_num_2))
        log.debug("%s,%s,%s" % (delete_num_0, delete_num_1, delete_num_2))
        self.assertTrue(realDeltrue)
        self.assertEqual(fact_result, respect_result)
