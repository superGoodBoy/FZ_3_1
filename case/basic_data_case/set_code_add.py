#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from CINTEL_FZWEB3_1_2_1.logger.log import Log
"""
局点编号 添加
"""
log=Log()
class Set_code(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        url = "http://192.168.2.87:8080/rg_web/index.shtml"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def add(self):
        driver=self.driver
        self.driver.find_element_by_id("login_name").send_keys("itim")
        self.driver.find_element_by_id("password").send_keys("itim204")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:10])
        click_btn = self.driver.find_elements_by_class_name("desktop-app")[47]

        action=ActionChains(driver)
        write=self.driver.find_elements_by_tag_name("legend")[5]
        action.move_to_element(write).perform()
        click_btn.click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))

    def test_add_operate_empty(self):
        log.info("7.1.1用例-添加，运营商选择框输入为空")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("88888")
        driver.find_elements_by_name("set_name")[1].send_keys("商业街二街")
        driver.find_element_by_name("machine_room").send_keys("银行")
        driver.find_element_by_name("set_address").send_keys("北京省北京市商业街二街银行")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()
        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_set_networktype_empty(self):
        log.info("7.1.2用例-添加：网络类型项输入为空")
        self.add()
        driver=self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("201334")
        driver.find_elements_by_name("set_name")[1].send_keys("中央大道中书省")
        driver.find_element_by_name("machine_room").send_keys("中央带中")
        driver.find_element_by_name("set_address").send_keys("北京省北京市中央公园博物馆")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        # driver.find_elements_by_tag_name('a')[5].click()
        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write =self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)

    def test_add_setcoordinate_empty(self):
        log.info("7.1.3用例-添加：局点坐标输入为空")
        self.add()
        driver=self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys(" ")
        driver.find_element_by_name("set_code").send_keys("201334")
        driver.find_elements_by_name("set_name")[1].send_keys("中央大道中书省")
        driver.find_element_by_name("machine_room").send_keys("中央带中")
        driver.find_element_by_name("set_address").send_keys("北京省北京市中央公园博物馆街")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name="必填项不能为空"
        self.assertEqual(fact_name,expect_name)

    def test_add_setcode_empty(self):
        log.info("7.1.4用例-添加：局点编号输入为空")
        self.add()
        driver = self.driver
        # log.info("添加输入框：%s" %driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]"))
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        # log.warning("据点编号输入框输入:%s" %driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input"))
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys(" ")
        driver.find_elements_by_name("set_name")[1].send_keys("中央大道中书省")
        driver.find_element_by_name("machine_room").send_keys("中央带中")
        driver.find_element_by_name("set_address").send_keys("北京省北京市中央公园博物馆f街")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_setname_empty(self):
        log.info("7.1.5用例-添加：局点名称输入为空")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("201334")
        driver.find_elements_by_name("set_name")[1].send_keys(" ")
        driver.find_element_by_name("machine_room").send_keys("中央带中")
        driver.find_element_by_name("set_address").send_keys("北京省北京市中央公园博物馆街")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_machine_room_empty(self):
        log.info("7.1.6用例-添加：机房名称项为空")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()

        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("201334")
        driver.find_elements_by_name("set_name")[1].send_keys("商业界")
        driver.find_element_by_name("machine_room").send_keys(" ")
        driver.find_element_by_name("set_address").send_keys("北京省北京市中央公园博物馆街")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()
        self.driver.implicitly_wait(30)
        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()

        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_setaddress_empty(self):
        log.info("7.1.7用例-添加：机房地址输入为空")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()

        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("201334")
        driver.find_elements_by_name("set_name")[1].send_keys("商业街")
        driver.find_element_by_name("machine_room").send_keys("银行")
        driver.find_element_by_name("set_address").send_keys(" ")

        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_province_empty(self):
        log.info("7.1.8用例-添加：省份下拉框选择为空")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("201334")
        driver.find_elements_by_name("set_name")[1].send_keys("法考发酵")
        driver.find_element_by_name("machine_room").send_keys("发大水佛兰")
        driver.find_element_by_name("set_address").send_keys("睡觉奥飞骄傲发货单")
        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "必填项不能为空"
        self.assertEqual(fact_name, expect_name)

    def test_add_setcoordinate_rule(self):
        log.info("7.2.1用例-添加：局点坐标输入规范")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        log.info("局点坐标项规范性输入")
        driver.find_element_by_name("set_coordinate").send_keys("2,32")
        driver.find_element_by_name("set_code").send_keys("13445")
        driver.find_elements_by_name("set_name")[1].send_keys("法考发酵")
        driver.find_element_by_name("machine_room").send_keys("发大水佛兰")
        driver.find_element_by_name("set_address").send_keys("睡觉奥飞骄傲发货单")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "不符合坐标规范,格式为[xxx,xxx]"
        self.assertEqual(fact_name, expect_name)

    def test_add_setcode_rule(self):
        log.info("7.2.2用例-添加：局点编号输入规范")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("发送到佛集群")
        driver.find_elements_by_name("set_name")[1].send_keys("法考发酵")
        driver.find_element_by_name("machine_room").send_keys("发大水佛兰")
        driver.find_element_by_name("set_address").send_keys("睡觉奥飞骄傲发货单")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()
        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name = "不符合局点编号规范"
        self.assertEqual(fact_name, expect_name)

    def test_add_setcodeexsits(self):
        log.info("7.3用例-添加：数据已存在校验")
        self.add()
        driver=self.driver
        self.driver.implicitly_wait(30)
        # log.info("添加输入框点击:%s" % driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]"))
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        log.info("国家代码项输入：%s" %driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input"))
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("13445")
        driver.find_elements_by_name("set_name")[1].send_keys("中央大道中书省二街")
        driver.find_element_by_name("machine_room").send_keys("学校")
        driver.find_element_by_name("set_address").send_keys("北京省北京市中央公园博物馆街")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        self.driver.implicitly_wait(30)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_elements_by_class_name("layui-layer-content")[1].text
        log.debug(fact_name)
        expect_name="局点编号或者局点名称已存在"
        self.assertEqual(fact_name,expect_name)

    def test_add_setcode_success(self):
        log.info("7.4用例-添加，成功保存")
        self.add()
        driver = self.driver
        driver.find_element_by_css_selector("body > div > div:nth-child(2) > div > div > button:nth-child(1)").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/button[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[1]/div/div/dl/dd[3]").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[2]/div/div/dl/dd[4]").click()
        driver.find_element_by_name("set_coordinate").send_keys("[2,322]")
        driver.find_element_by_name("set_code").send_keys("88888")
        log.info("输入局点定位: %s "% driver.find_elements_by_name("set_name")[1].text)
        driver.find_elements_by_name("set_name")[1].send_keys("商业街二街")
        driver.find_element_by_name("machine_room").send_keys("银行")
        driver.find_element_by_name("set_address").send_keys("北京省北京市商业街二街银行")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/div/input").click()
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div")
        driver.find_element_by_xpath("//*[@id='saveSetCodeId']/div[8]/div/div/dl/dd[2]").click()

        click_btn = self.driver.find_element_by_class_name("layui-layer-btn0")
        action = ActionChains(driver)
        self.driver.implicitly_wait(30)
        write = self.driver.find_element_by_class_name("layui-layer-btn0")
        action.move_to_element(write).perform()
        click_btn.click()
        time.sleep(1.5)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        log.debug(fact_name)
        expect_name = "添加成功"
        self.assertEqual(fact_name, expect_name)

# import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# if __name__ == '__main__':
#
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Set_code)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2局点编号添加功能",
#         description='测试报告',
#     )
#     runner.run(suite)