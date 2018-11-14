#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from time import sleep
"""
缺陷：只能查询当前2018年前半年的数据，其他年份不能查询
 
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

class intercept_clibarring(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=65cc0fb4-3dd3-4c1f-94db-a167d1b66d39")

    def login(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("ca_system_admin")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("vcode").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        sleep(4)
        driver.find_element_by_css_selector("body > div.container-fluid > div.swiper-container.swiper-container-w.swiper-container-horizontal > div.swiper-wrapper > div:nth-child(4) > fieldset").click()
        driver.find_element_by_xpath("//*[@id='selectData']/div[2]/div/i").click()
        # driver.find_element_by_xpath("//*[@id='selectData']/div[1]/div/i").click()
        sleep(2)
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))

     # 主叫黑名单精确号码拦截
    def test_number_12(self):
        self.login()
        barringtype=1
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[2]").click()   #拦截类型

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            print(all_number)
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
                           AND barringtype='%s'
                       """ % (calling_number, date1, date2,barringtype)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else :
            no_data = self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1="无数据"
            print(no_data,no_data1)
            self.assertEqual(no_data,no_data1)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    # 主叫黑名单号段拦截 ----

    def test_number_13(self):
        self.login()
        barringtype = 2
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[3]").click()   #拦截类型

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            print(all_number)
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
                           AND barringtype='%s'
                       """ % (calling_number, date1, date2,barringtype)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1,no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        # 原被叫黑名单拦截 ----error

    def test_number_14(self):
        self.login()
        barringtype = 3
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[4]").click()  # 拦截类型

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            print(all_number)
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
                             AND barringtype='%s'
                         """ % (calling_number, date1, date2,barringtype)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        # 被叫按键拦截 ----

    def test_number_15(self):
        self.login()
        barringtype = 4
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[5]").click()  # 拦截类型

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            print(all_number)
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
                           """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

     # 主叫后N位公检法号码模糊匹配拦截 ----

    def test_number_16(self):
        self.login()
        barringtype = 5
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[6]").click()  # 拦截类型

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
        catch_text = self.driver.find_element_by_css_selector(".layui-tab").text
        import re
        calling_content = re.findall(r'\d+\.?\d*', catch_text)
        all_number = calling_content.__len__() - 10
        if all_number>=0:
            print(all_number)
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
                               AND barringtype='%s'
                           """ % (calling_number, date1, date2,barringtype)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    # 主叫非法国家代码呼叫拦截  -
    def test_number_17(self):
        self.login()
        barringtype = 6
        calling_number = "8613942395520"
        date1 ="2018-01-01"
        date2 ="2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' %(date1,date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[7]").click()  # 拦截类型

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
        catch_text=self.driver.find_element_by_css_selector(".layui-tab").text
        import  re
        calling_content =re.findall(r'\d+\.?\d*',catch_text)
        all_number =calling_content.__len__()-10
        print(all_number)
        if all_number>=0:
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
                        AND barringtype='%s'
                    """ %(calling_number,date1,date2,barringtype)).__len__()
            print(time_fact,time_expcect)
            self.assertEqual(time_fact,time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    # 主叫位长超长或超短拦截   --error
    def test_number_18(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[8]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                              AND  barringtype = 7
                           """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

     # 主叫号码为空拦截
    def test_number_19(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[9]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 8
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

     # 主叫虚假公安语音识别拦截
    def test_number_20(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[10]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 9
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

   # 虚假400号码拦截
    def test_number_21(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[11]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 10
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    # 时间 + 主叫 + 原被叫 + 拦截类型：主叫灰名单在线语音识别拦截
    def test_number_22(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[12]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 11
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    # 时间 + 主叫 + 原被叫 + 拦截类型：主叫号码隐藏拦截
    def test_number_23(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[13]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 12
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    # 时间 + 主叫 + 原被叫 + 拦截类型：假冒国际漫游
    def test_number_24(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[14]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 13
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    # 时间 + 主叫 + 原被叫 + 拦截类型：假冒国内漫游

    def test_number_25(self):
        self.login()
        calling_number = "0085266329500"
        date1 = "2018-01-01"
        date2 = "2018-04-07"
        js = 'document.getElementById("LAY_demorange_se").value="%s 00:00:00 - %s 23:59:59"' % (date1, date2)
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[2]/div/input").send_keys(calling_number)

        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[5]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[5]/div/div/dl/dd[15]").click()

        self.driver.find_element_by_xpath("//form[@id='conditionForm']/div/button").click()
        sleep(30)
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
                                 AND  barringtype = 14
                              """ % (calling_number, date1, date2)).__len__()
            print(time_fact, time_expcect)
            self.assertEqual(time_fact, time_expcect)
        else:
            no_data = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div").text
            no_data1 = "无数据"
            print(no_data, no_data1)
            self.assertEqual(no_data1, no_data)
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

# if __name__ == "intercept_clibarring.py":
#     report_dir = r's.html'
#     re_open = open(report_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(intercept_clibarring)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title=u'FZ系统web3.1.2拦截话单查询',
#         description=u'FZ系统web3.1.2拦截话单查询测试详情'
#     )
#     runner.run(suite)