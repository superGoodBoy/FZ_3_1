#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *

"""
1.时间+主叫                                      校验条数
2.时间+主叫+呼叫类型：前端服务器过载               校验条数
3.时间+主叫+呼叫类型：正常挂机                    校验条数
4.时间+主叫+呼叫类型：在线语音识别异常      校验条数
5.时间+主叫+原被叫+呼叫类型：前端bypass           校验条数
6.时间+主叫+原被叫+呼叫类型：MS bypass            校验条数
7.时间+主叫+原被叫+呼叫类型：CPU过载拒绝呼叫       校验条数
8.时间+主叫+原被叫+呼叫类型：capS超限bypass       校验条数
9.时间+主叫+原被叫+呼叫类型：拦截平台外呼          校验条数
10.时间+主叫+原被叫+呼叫类型：其他                校验条数

"""

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def login(self):
        driver = self.driver
        driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=65cc0fb4-3dd3-4c1f-94db-a167d1b66d39")
        driver.find_element_by_id("login_name").send_keys("ca_system_admin")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("vcode").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(4)
        # driver.find_element_by_xpath("//div[@id='selectData']/div/div/i").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | index=0 | ]]
        driver.find_element_by_css_selector("body > div.container-fluid > div.swiper-container.swiper-container-w.swiper-container-horizontal > div.swiper-wrapper > div:nth-child(4) > fieldset").click()
        driver.find_element_by_xpath("//*[@id='selectData']/div[1]/div/i").click()
        time.sleep(2)
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))
    # 时间加主叫
    def test_number_1(self):
        self.login()
        calling_number = "8613942395520"
        date1 ="2017-03-26 "
        date2 ="2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s - %s"' %(date1,date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_id("callingnumber").send_keys(calling_number)
        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(7)
        catch_text=self.driver.find_element_by_css_selector(".layui-tab").text
        import  re
        calling_content =re.findall(r'\d+\.?\d*',catch_text)
        all_number =calling_content.__len__()-10
        time_fact =int(calling_content[all_number])
        time_expcect=getmysql(sql="""
                   SELECT
                        *
                    FROM
                        call_barring_2018_first
                    WHERE
                        callingnumber = '%s'
                    AND starttime >= '%s 00:00:00'
                    AND endtime <= '%s 23:59:59'
                """ %(calling_number,date1,date2) ).__len__()
        print(time_fact,time_expcect)
        self.assertEqual(time_fact,time_expcect)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    # 正常挂机
    def test_number_3(self):
        self.login()
        calling_number = "13701722443"
        date1 = "2017-03-26 "
        date2 = "2018-04-07"
        js_date = 'document.getElementById("LAY_demorange_se").value="%s - %s"' % (date1, date2)
        self.driver.execute_script(js_date)
        self.driver.find_element_by_id("callingnumber").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(7)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        time_fact = int(calling_content[all_number])
        time_expcect = getmysql(sql="""
                          SELECT
                               *
                           FROM
                               call_barring_2018_first
                           WHERE
                               callingnumber = '%s'
                           AND starttime >= '%s 00:00:00'
                           AND endtime <= '%s 23:59:59'
                          AND  calltype = 0
                       """ % (calling_number, date1, date2)).__len__()
        print(time_fact, time_expcect)
        self.assertEqual(time_fact, time_expcect)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    # ---------------------------------------------------------------------
    """
    11. 时间 + 主叫 + 原被叫 + 拦截类型：未拦截 校验条数
    12.时间 + 主叫 + 原被叫 + 拦截类型：主叫黑名单精确号码拦截 校验条数
    13.时间 + 主叫 + 原被叫 + 拦截类型：主叫黑名单号段拦截 校验条数
    14.时间 + 主叫 + 原被叫 + 拦截类型：原被叫黑名单拦截 校验条数
    15.时间 + 主叫 + 原被叫 + 拦截类型：被叫按键拦截 校验条数
    16.时间 + 主叫 + 原被叫 + 拦截类型：主叫后N位公检法号码模糊匹配拦截（N可配）         校验条数
    17.时间 + 主叫 + 原被叫 + 拦截类型：主叫非法国家代码呼叫拦截 校验条数
    18.时间 + 主叫 + 原被叫 + 拦截类型：主叫位长超长或超短拦截 校验条数
    19.时间 + 主叫 + 原被叫 + 拦截类型：主叫号码为空拦截 校验条数
    20.时间 + 主叫 + 原被叫 + 拦截类型：主叫虚假公安呼叫拦截 校验条数
    21.时间 + 主叫 + 原被叫 + 拦截类型：虚假400号码拦截 校验条数
    22.时间 + 主叫 + 原被叫 + 拦截类型：主叫灰名单在线语音识别拦截 校验条数
    23.时间 + 主叫 + 原被叫 + 拦截类型：主叫号码隐藏拦截 校验条数
    24.时间 + 主叫 + 原被叫 + 拦截类型：假冒国际漫游 校验条数
    25.时间 + 主叫 + 原被叫 + 拦截类型：假冒国内漫游 校验条数
    """
    def test_number_11(self):
        self.login()
        calling_number = "01057684732"
        date1 = "2017-03-26 "
        date2 = "2018-04-07"
        js_date = 'document.getElementById("LAY_demorange_se").value="%s - %s"' % (date1, date2)
        self.driver.execute_script(js_date)
        self.driver.find_element_by_id("callingnumber").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[6]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[6]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[6]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(1)
        load_fact=self.driver.find_element_by_xpath("//*[@id='loading']").text
        load_expect="加载中..."
        time.sleep(5)
        self.assertEqual(load_expect,load_fact)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            time_fact = int(calling_content[all_number])
            time_expcect = getmysql(sql="""
                              SELECT
                                   *
                               FROM
                                   call_barring_2018_first
                               WHERE
                                   callingnumber = '%s'
                               AND starttime >= '%s 00:00:00'
                               AND endtime <= '%s 23:59:59'
                               AND  barringtype =1
                           """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            print("拦截类型为：主角黑名单精确号码查询没有数据 或 加载过程等待时间过短 或 后端类型与数字不匹配")
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_number_23(self):
        self.login()
        calling_number = "0085259329725"
        date1 = "2017-03-26 "
        date2 = "2018-04-07"
        js_date = 'document.getElementById("LAY_demorange_se").value="%s - %s"' % (date1, date2)
        self.driver.execute_script(js_date)
        self.driver.find_element_by_id("callingnumber").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[6]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[6]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[6]/div/div/dl/dd[14]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        time.sleep(2)
        load_fact = self.driver.find_element_by_xpath("//*[@id='loading']").text
        load_expect = "加载中..."
        time.sleep(10)
        self.assertEqual(load_fact,load_expect)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            time_fact = int(calling_content[all_number])
            time_expcect = getmysql(sql="""
                              SELECT
                                   *
                               FROM
                                   call_barring_2018_first
                               WHERE
                                   callingnumber = '%s'
                               AND starttime >= '%s 00:00:00'
                               AND endtime <= '%s 23:59:59'
                              AND  calltype = 0
                           """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            print("拦截类型为：主叫号码隐藏拦截类型 没有该数据")
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
