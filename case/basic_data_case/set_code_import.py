#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren

from selenium import webdriver
import unittest,time,redis
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.logger.log import *
log=Log()

r = redis.Redis(host='192.168.2.51', port=7111)
text_1 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(" ")
r = redis.Redis(host='192.168.2.51', port=7112)
text_2 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(" ")
r = redis.Redis(host='192.168.2.52', port=7111)
text_3 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(" ")
r = redis.Redis(host='192.168.2.52', port=7112)
text_4 = " ".join(re.findall(r"\d+\.?\d*", " ".join(sorted([str(i) for i in r.keys("specnumber_*")])))).split(" ")
# r.flushall()

class Set_code(unittest.TestCase):
    def setUp(self):
        log.info("特殊短号码导入：开始测试")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("特殊短号码导入：结束测试")
        driver = self.driver
        driver.close()

    def import_setcode(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[47]
        from selenium.webdriver.common.action_chains import ActionChains
        action=ActionChains(driver)
        write=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[6]/fieldset/legend")
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_importDocument_allZero(self):
        log.info('模板内容全部为空导入验证:局点编号moban2018年05月07日17时03分47秒')
        self.import_setcode()
        time.sleep(0.8)
        self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[4]/i").click()
        time.sleep(0.8)
        callexe(exe_file="setcode_Document_allZero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile\basic_data")
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.info(fact_result)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"Excel文件中没有任何数据"
        self.assertEqual(fact_result, expect_result)

    def test_importOtherDocument_allZero(self):
        u'模板导入其他模板查看是否导入成功:主叫白名单号码模版2018年02月06日14时30分16秒'
        self.import_setcode()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[4]/i").click()
        time.sleep(0.8)
        callexe(exe_file="area_OtherDocument_allZero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile\basic_data")
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.info(fact_result)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"sheet的名称应为局点编号"
        self.assertEqual(fact_result, expect_result)

    def test_importDocument_successs(self):
        log.info(u'模板导入并验证：局点编号模版2018年05月07日17时03分41秒')
        self.import_setcode()
        time.sleep(0.8)
        self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[4]/i").click()
        time.sleep(0.8)
        callexe(exe_file="setcode_Document_success.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile\basic_data")
        WebDriverWait(self.driver, 50).until(
            lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.info(fact_result)
        self.driver.implicitly_wait(30)
        # self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        # self.driver.switch_to.default_content()
        # self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        # time.sleep(2)
        # self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        expect_result = u"成功导入全部数据"
        self.assertEqual(fact_result, expect_result)

if __name__ == '__main__':
    unittest.main()