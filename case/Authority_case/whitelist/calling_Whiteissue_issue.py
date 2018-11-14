# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
import unittest, time,re
from CINTEL_FZWEB3_1_2_1.logger.log import *

"""
------------下发
1待审核 不选直接点击下发
2已审核 不选直接点击下发
3已撤销 不选直接点击下发 
4已过期 不选直接点击下发
5待审核   下发
5_5        5tiao xioafa  
6已审核    残损部分运营商状态下发失败 下发  --未编写
7已撤销   下发
7_5        5tiaoxiafa 
8已过期   下发
8_5        5tiao xiafa 

"""
import pymysql as mdb
def getmysql(sql):
    con = mdb.connect("192.168.2.87", "root", "123456", "rg_web3_1")
    with con:
        cursor = con.cursor()
        cursor.execute(sql)
        num_status_tuple = cursor.fetchall()
    return num_status_tuple

log=Log()
class Issue(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        log.info("打开浏览器")
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

    def test_issue_empty_1(self):
        "待审核点击选择要下发的行"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        print(fact_name)
        expect_name = "请选择要下发的行"
        self.assertEqual(expect_name, fact_name)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_issue_empty_2(self):
        u"已审核不选择直接点击下发按钮"
        driver=self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        time.sleep(2)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expect_name="请选择要下发的行"
        self.assertEqual(expect_name,fact_name)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_issue_empty_3(self):
        "已撤销 页面不选择直接点击下发按钮"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[3]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "请选择要下发的行"
        self.assertEqual(expect_name, fact_name)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_issue_empty_4(self):
        u"已过期直接点击 下发"
        driver =self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[4]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        time.sleep(2)
        fact_name = driver.find_element_by_class_name("layui-layer-content").text
        expect_name = "请选择要下发的行"
        self.assertEqual(expect_name, fact_name)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_issue_success_1(self):
        "待审核 选择数据下发"
        driver = self.driver
        self.login()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/div/div/i").click()
        content_text =driver.find_element_by_class_name("mailbox-controls").text
        number_text =content_text.split("主叫号码")[2]
        number_text_history=(re.findall(r"\d+\.?\d*",number_text)[00])
        number_status_history =getmysql(sql="""
                                        SELECT
                                            ct_deliver_status,
                                            cm_deliver_status,
                                            cu_deliver_status,
                                            cr_deliver_status
                                        FROM
                                            t_whitelist
                                        WHERE
                                            calling_number = '%s'
                                        """%number_text_history )
        ct_operator_status=list(number_status_history)[0][0]
        cm_operator_status=list(number_status_history)[0][1]
        cu_operator_status=list(number_status_history)[0][2]
        cr_operator_status=list(number_status_history)[0][3]
        print("下发前各运营商状态:",number_text_history,ct_operator_status,cm_operator_status,cu_operator_status,cr_operator_status)
        # 下发点击
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[1]/i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()
        time.sleep(0.5)
        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定下发吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(5)

        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        content_text = driver.find_element_by_class_name("mailbox-controls").text
        number_text_now = content_text.split("主叫号码")[2]
        number_text_n = re.findall(r"\d+\.?\d*", number_text_now)[00]
        self.assertEqual(number_text_history,number_text_n)

        number_status=getmysql(sql="""
                                SELECT
                                  	ct_deliver_status,
                                    cm_deliver_status,
                                    cu_deliver_status,
                                    cr_deliver_status
                                FROM
                                    t_whitelist
                                WHERE
                                    calling_number = '%s'
                                """%number_text_history )
        num_status_={}
        ct_operator_status_now = list(number_status)[0][0]
        cm_operator_status_now = list(number_status)[0][1]
        cu_operator_status_now = list(number_status)[0][2]
        cr_operator_status_now = list(number_status)[0][3]
        # num_status_[number_text_history+'_status']=list(number_status)[0][0]
        print("下发后各运营商状态:",number_text_history,ct_operator_status_now,cm_operator_status_now,cu_operator_status_now,cr_operator_status_now)

    def test_issue_moresuccess_1(self):
        "待审核 选择数据下发"
        driver = self.driver
        self.login()
        m=0
        time.sleep(3)
        for i in range(5):
            i+=1
            content_1="/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr["
            conten_3=str(i)
            content_2="]/td[1]/div/div/i"
            self.driver.find_element_by_xpath(content_1+conten_3+content_2).click()
        content_text =driver.find_element_by_class_name("mailbox-controls").text.split("主叫号码")[2]
        nume_list_history=[]
        number_list_data=re.findall(r"\d+\.?\d*",content_text)
        for i in  range(5):
            nume_list_history.append(number_list_data[i])
        nume_list_history.sort()
        print(nume_list_history)
        dict_status_history={}

        number_status =getmysql(sql="""
                                        SELECT
                                            ct_deliver_status,
                                            cm_deliver_status,
                                            cu_deliver_status,
                                            cr_deliver_status
                                        FROM
                                            t_whitelist
                                        WHERE
                                        calling_number = '%s'
                                        or  calling_number = '%s'
                                        or  calling_number = '%s'
                                        or  calling_number = '%s'
                                        or  calling_number = '%s'
                                        """%(nume_list_history[0],nume_list_history[1],nume_list_history[2],nume_list_history[3],nume_list_history[4])  )
        for i in number_status:
            dict_status_history[nume_list_history[m]+'_num_status']=i
            m+=1
        print("下发前各运营商状态:%s"%dict_status_history)
        # 下发点击
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[1]/i").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()

        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定下发吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(2)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        content_text_now = driver.find_element_by_class_name("mailbox-controls").text.split("主叫号码")[2]
        nume_list_now = []
        number_list_now = re.findall(r"\d+\.?\d*", content_text_now)
        for m in range(5):
            nume_list_now.append(number_list_now[m])
        nume_list_now.sort()
        print(nume_list_now)
        self.assertEqual(nume_list_now,nume_list_history)
        dict_status_now = {}
        number_status_now =getmysql(sql="""
                                        SELECT
                                            ct_deliver_status,
                                            cm_deliver_status,
                                            cu_deliver_status,
                                            cr_deliver_status
                                        FROM
                                            t_whitelist
                                        WHERE
                                        calling_number = '%s'
                                        or  calling_number = '%s'
                                        or  calling_number = '%s'
                                        or  calling_number = '%s'
                                        or  calling_number = '%s'
                                        """%(nume_list_history[0],nume_list_history[1],nume_list_history[2],nume_list_history[3],nume_list_history[4])  )
        n=0
        for i in number_status_now:
            dict_status_now[nume_list_history[n]+'_num_status']=i
            n+=1
        print("下发后各运营商状态:%s"%dict_status_now)

    # def test_6(self):
    #     u"已审核选择残损数据点击下发按钮"
        # driver = self.driver
        # self.login()
        # time.sleep(5)
        # driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        # time.sleep(2)
        # fact_name = driver.find_element_by_class_name("layui-layer-content").text
        # expect_name = "请选择要下发的行"
        # self.assertEqual(expect_name, fact_name)
        # pass

    def test_issue_fail_2(self):
        u"已审核选择点击下发按钮"
        driver=self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        self.driver.implicitly_wait(30)
        driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/div/div/i").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button/i").click()
        time.sleep(2)
        fact_name=driver.find_element_by_class_name("layui-layer-content").text
        expect_name="没有符合下发条件的号码，不需要下发！"
        self.assertEqual(expect_name,fact_name)
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_issue_success_3(self):
        "已撤销 页面"
        driver = self.driver
        self.login()
        time.sleep(3)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[3]").click()

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
        print("下发前各运营商状态:", ct_operator_status, cm_operator_status, cu_operator_status, cr_operator_status)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[1]/i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()
        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定下发吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
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
        # self.assertEqual(number_status,number_status_history+1)
        ct_operator_status_now = list(number_status)[0][0]
        cm_operator_status_now = list(number_status)[0][1]
        cu_operator_status_now = list(number_status)[0][2]
        cr_operator_status_now = list(number_status)[0][3]
        print("下发后各运营商状态:", ct_operator_status_now, cm_operator_status_now, cu_operator_status_now,
              cr_operator_status_now)

    def test_issue_moresuccess_3(self):
        "已撤销"
        driver = self.driver
        self.login()
        time.sleep(2)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[3]").click()
        m = 0
        time.sleep(3)
        for i in range(5):
            i += 1
            content_1 = "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr["
            conten_3 = str(i)
            content_2 = "]/td[1]/div/div/i"
            self.driver.find_element_by_xpath(content_1 + conten_3 + content_2).click()
        content_text = driver.find_element_by_class_name("mailbox-controls").text.split("主叫号码")[2]
        nume_list_history = []
        number_list_data = re.findall(r"\d+\.?\d*", content_text)
        for i in range(5):
            nume_list_history.append(number_list_data[i])
        nume_list_history.sort()
        print(nume_list_history)
        dict_status_history = {}

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
                                                or  calling_number = '%s'
                                                or  calling_number = '%s'
                                                or  calling_number = '%s'
                                                or  calling_number = '%s'
                                                """ % (
        nume_list_history[0], nume_list_history[1], nume_list_history[2], nume_list_history[3], nume_list_history[4]))
        for i in number_status:
            dict_status_history[nume_list_history[m] + '_num_status'] = i
            m += 1
        print("下发前各运营商状态:", dict_status_history)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[1]/i").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()
        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定下发吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        content_text_now = driver.find_element_by_class_name("mailbox-controls").text.split("主叫号码")[2]
        nume_list_now = []
        number_list_now = re.findall(r"\d+\.?\d*", content_text_now)
        for m in range(5):
            nume_list_now.append(number_list_now[m])
        nume_list_now.sort()
        print(nume_list_now)
        self.assertEqual(nume_list_now, nume_list_history)
        dict_status_now = {}
        number_status_now = getmysql(sql="""
                                                SELECT
                                                    ct_deliver_status,
                                                    cm_deliver_status,
                                                    cu_deliver_status,
                                                    cr_deliver_status
                                                FROM
                                                    t_whitelist
                                                WHERE
                                                calling_number = '%s'
                                                or  calling_number = '%s'
                                                or  calling_number = '%s'
                                                or  calling_number = '%s'
                                                or  calling_number = '%s'
                                                """ % (
        nume_list_history[0], nume_list_history[1], nume_list_history[2], nume_list_history[3], nume_list_history[4]))
        n = 0
        for i in number_status_now:
            dict_status_now[nume_list_history[n] + '_num_status'] = i
            n += 1
        print("下发后各运营商状态:", dict_status_now)

    def test_issue_success_4(self):
        u"已过期"
        driver = self.driver
        self.login()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div/div[2]/div/div/ul/li[4]").click()

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
        print("下发前各运营商状态:", ct_operator_status, cm_operator_status, cu_operator_status, cr_operator_status)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[1]/i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()

        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定下发吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(5)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
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
        # self.assertEqual(number_status,number_status_history+1)
        ct_operator_status_now = list(number_status)[0][0]
        cm_operator_status_now = list(number_status)[0][1]
        cu_operator_status_now = list(number_status)[0][2]
        cr_operator_status_now = list(number_status)[0][3]
        print("下发后各运营商状态:", ct_operator_status_now, cm_operator_status_now, cu_operator_status_now,
              cr_operator_status_now)

    def test_issue_moresuccess_4(self):
        "已过期（5）"
        driver = self.driver
        self.login()
        time.sleep(2)
        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[4]").click()
        m = 0
        time.sleep(3)
        for i in range(5):
            i += 1
            content_1 = "/html/body/div/div[2]/div/div/div/div/div[3]/div[2]/table/tbody/tr["
            conten_3 = str(i)
            content_2 = "]/td[1]/div/div/i"
            self.driver.find_element_by_xpath(content_1 + conten_3 + content_2).click()
        content_text = driver.find_element_by_class_name("mailbox-controls").text.split("主叫号码")[2]
        nume_list_history = []
        number_list_data = re.findall(r"\d+\.?\d*", content_text)
        for i in range(5):
            nume_list_history.append(number_list_data[i])
        nume_list_history.sort()
        print(nume_list_history)
        dict_status_history = {}

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
                                                       or  calling_number = '%s'
                                                       or  calling_number = '%s'
                                                       or  calling_number = '%s'
                                                       or  calling_number = '%s'
                                                       """ % (
            nume_list_history[0], nume_list_history[1], nume_list_history[2], nume_list_history[3],
            nume_list_history[4]))
        for i in number_status:
            dict_status_history[nume_list_history[m] + '_num_status'] = i
            m += 1
        print("下发前各运营商状态:", dict_status_history)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/button[1]/i").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[3]/button[1]/i").click()

        real_t = driver.find_element_by_xpath("//*[@id='LAY_layuipro']/div").text
        text = "确定下发吗？"
        self.assertEqual(real_t, text)
        driver.find_element_by_css_selector(
            "html body div#layui-layer1.layui-layer.layui-layer-page div.layui-layer-btn.layui-layer-btn- a.layui-layer-btn0").click()
        time.sleep(5)

        driver.find_element_by_xpath("/ html/body/div/div[2]/div/div/ul/li[2]").click()
        content_text_now = driver.find_element_by_class_name("mailbox-controls").text.split("主叫号码")[2]
        nume_list_now = []
        number_list_now = re.findall(r"\d+\.?\d*", content_text_now)
        for m in range(5):
            nume_list_now.append(number_list_now[m])
        nume_list_now.sort()
        print(nume_list_now)
        self.assertEqual(nume_list_now, nume_list_history)
        dict_status_now = {}
        number_status_now = getmysql(sql="""
                               SELECT
                                   ct_deliver_status,
                                   cm_deliver_status,
                                   cu_deliver_status,
                                   cr_deliver_status
                               FROM
                                   t_whitelist
                               WHERE
                               calling_number = '%s'
                               or  calling_number = '%s'
                               or  calling_number = '%s'
                               or  calling_number = '%s'
                               or  calling_number = '%s'
                               """ % (
            nume_list_history[0], nume_list_history[1], nume_list_history[2], nume_list_history[3],
            nume_list_history[4]))
        n = 0
        for i in number_status_now:
            dict_status_now[nume_list_history[n] + '_num_status'] = i
            n += 1
        print("下发后各运营商状态:", dict_status_now)
#
# if __name__ == 'calling_Whiteissue_issue.py':
#     reporter_dir = r's.html'
#     re_open = open(reporter_dir, 'wb')
#     suite = unittest.TestLoader().loadTestsFromTestCase(Issue)
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2主叫白名单下发下发操作",
#         description='测试情况',
#     )
#     runner.run(suite)