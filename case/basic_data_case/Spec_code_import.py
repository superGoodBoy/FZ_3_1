#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
#  allzero
# success

"""
specnumnberq

"""
from selenium.webdriver.support.wait import WebDriverWait
from selenium import  webdriver
import unittest,time,redis
from selenium.common.exceptions import NoSuchElementException
from CINTEL_FZWEB3_1_2_1.logger.log import *
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
log=Log()
try:
    r = redis.Redis(host='192.168.2.51', port=7111)
    r.delete('special_number_list')
    r = redis.Redis(host='192.168.2.51', port=7112)
    r.delete('special_number_list')
    r = redis.Redis(host='192.168.2.52', port=7111)
    r.delete('special_number_list')
    r = redis.Redis(host='192.168.2.52', port=7112)
    r.delete('special_number_list')
    r = redis.Redis(host='192.168.2.130', port=7111)
    r.delete('special_number_list')
    r = redis.Redis(host='192.168.2.130', port=7112)
    r.delete('special_number_list')
except Exception as e:
    print(e)
from rediscluster import StrictRedisCluster
nodes =[{'host':'192.168.2.130','port':'7111'}]
r =StrictRedisCluster(startup_nodes=nodes,decode_responses=True)
r.delete('special_number_list')

class Spec_code(unittest.TestCase):
    def setUp(self):
        log.info("特殊短号码导入：开始测试")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("特殊短号码导出：结束测试")
        driver = self.driver
        driver.close()

    def import_speccode(self):
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
        write=self.driver.find_elements_by_class_name("desktop-app")[49]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_importDocument_allZero(self):
        u'模板内容全部为空导入验证:特殊短号码模板2018年05月08日09时52分35秒 '
        self.import_speccode()
        self.driver.implicitly_wait(30)
        log.info("按钮识别：%s" % self.driver.find_element_by_xpath("//i[contains(text(),'')]").get_attribute("title"))

        self.driver.find_element_by_xpath("//i[contains(text(),'')]").click()
        time.sleep(1)
        callexe(exe_file="spec_Document_allZero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile\basic_data")
        try:
            WebDriverWait(self.driver,20).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
            fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        except NoSuchElementException as e:
            print(e)
            return False
        log.info(fact_result)
        expect_result = u"Excel文件中没有任何数据"
        self.assertEqual(fact_result, expect_result)

        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_importOtherDocument_allZero(self):
        u'模板导入其他模板查看是否导入成功:主叫白名单号码模版2018年02月06日14时30分16秒'
        self.import_speccode()
        self.driver.implicitly_wait(30)
        # log.info("按钮识别：%s" % self.driver.find_element_by_xpath("//i[contains(text(),'')]").get_attribute("title"))
        self.driver.find_element_by_xpath("//i[contains(text(),'')]").click()
        time.sleep(3)
        callexe(exe_file="area_OtherDocument_allZero.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile\basic_data")
        WebDriverWait(self.driver, 20).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.info(fact_result)
        expect_result = u"sheet的名称应为特殊短号码"
        self.assertEqual(fact_result, expect_result)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

    def test_importDocument_successs(self):
        u'模板导入并验证：特殊短号码模板2018年05月08日09时52分36秒'
        self.import_speccode()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div/button[4]/i").click()
        time.sleep(1)
        start=time.clock()
        callexe(exe_file="spec_Document_success.exe", exe_path=r"C:\Users\renqiwei\Desktop\study\exefile\basic_data")
        end=time.clock()
        log.info("used:%s" %(end-start))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-content"))
        fact_result = self.driver.find_element_by_class_name("layui-layer-content").text
        log.info(fact_result)
        expect_result = u"成功导入19条记录"
        self.assertEqual(fact_result, expect_result)
        self.driver.find_element_by_css_selector("div.layui-layer-btn.layui-layer-btn-").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        # self.driver.implicitly_wait(30)
        # self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[contains(text(),退出)]")

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == 'Spec_code_import':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Spec_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2特殊短号码导入功能",
#         description='测试报告',
#     )
#     runner.run(suite)