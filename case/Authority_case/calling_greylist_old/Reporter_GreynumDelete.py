# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# from CINTEL_FZweb3_1_1.tote_box.grid_module import *
from CINTEL_FZweb3_1_1.tote_box.getmysql_num import *
from CINTEL_FZweb3_1_1.tote_box.select_realdelete import *
# import importlib,sys
# importlib.reload(sys)
# # sys.setdefaultencoding( "utf-8" )
"""
运营商 灰名单录入删除测试

"""

class GreynumDelete(unittest.TestCase):
    def setUp(self):
        # for host, browser in grid_6().items():
        # # for host, browser in d().items():
        #     driver = webdriver.Remote(
        #         command_executor=host,
        #         desired_capabilities={
        #             'platform': 'ANY',
        #             'browserName': browser,
        #             'version': '',
        #             'javascriptEnabled': True
        #         }
        #     )
        self.data =[
            {"username":"ct_operator","password":"123456"},
        ]
        self.driver =webdriver.Chrome()
        self.driver.maximize_window()
        self.accept_next_alert = True
        self.driver.get("http://192.168.2.87:8081/rg_web/login.shtml")

    def greynum_delete(self,username,pwd):
        self.driver.find_element_by_id("login_name").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(pwd)
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//div[@id='taskOrder']/div/div/i").click()
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        time.sleep(3)

    def test_already_delete_a(self):
        "已推送不选数据直接删除ok"
        data_0 = self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname,pwd)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        time.sleep(5)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result="请选择要删除的行"
        self.assertEqual(fact_result,expect_result)



    def  test_current_user_push_delete_b(self):
        u"电信角色ct_operator选择自己添加的未下发状态删除"
        data_0 = self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        time.sleep(3)
        self.greynum_delete(uname, pwd)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()

        al_num = getmysql("""
                SELECT
                        calling_number,create_time,update_time
                    FROM
                        t_greylist
                    WHERE
                        creator_type=0
                        AND creator_type=0
                        AND ca_status=1
                        and ct_deliver_status=0
                        AND cr_deliver_status=0
                        and cm_deliver_status=0
                        and cu_deliver_status=0
                    ORDER BY
                        greylist_id
        """)

        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[2]/div/input").send_keys(al_num[4])
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/div").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()

        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result="删除成功"
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        true =getTrueOrFalse("""
                       select calling_number from  t_greylist where calling_number=%s
               """  %al_num[4])
        self.assertEqual(fact_result, expect_result)
        self.assertTrue(true)
        print(fact_result,true)

    def  test_current_user_push_delete_c(self):
        u"电信角色ct_operator选择自己添加的yi下发状态删除失败"
        data_0 = self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname, pwd)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()

        al_num = getmysql("""
                SELECT
                        calling_number,create_time,update_time
                    FROM
                        t_greylist
                    WHERE
                        creator_type=0
                        AND creator_type=0
                        AND ca_status=1
                        and ct_deliver_status=1
                    ORDER BY
                        greylist_id
        """)
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[2]/div/input").send_keys(al_num[4])
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/div").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()

        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result="不能删除下发已经生效的灰名单"
        self.assertEqual(fact_result,expect_result)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def  test_current_user_push_delete_d(self):
        u"电信角色ct_operator选择非系统添加的未下发状态删除"
        data_0 = self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname, pwd)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()

        al_num = getmysql("""
                SELECT
                        calling_number,create_time,update_time
                    FROM
                        t_greylist
                    WHERE
                        creator_type !=0
                        AND creator_type !=6
                        AND ca_status=1
                        and ct_deliver_status=0
                        AND cr_deliver_status=0
                        and cm_deliver_status=0
                        and cu_deliver_status=0
                    ORDER BY
                        greylist_id
        """)
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[2]/div/input").send_keys(al_num[4])
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/div").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()

        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result="不能删除非当前用户产生的灰名单"
        self.assertEqual(fact_result,expect_result)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_current_user_push_delete_e(self):
        u"电信角色ct_operator选择非系统添加的已下发状态删除"
        data_0 = self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname, pwd)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()

        al_num = getmysql("""
                  SELECT
                          calling_number,create_time,update_time
                      FROM
                          t_greylist
                      WHERE
                          creator_type !=0
                          AND creator_type !=6
                          AND ca_status=1
                          and (ct_deliver_status=1
                          or cr_deliver_status=1
                          or cm_deliver_status=1
                          or cu_deliver_status=1)
                      ORDER BY
                          greylist_id
          """)
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[2]/div/input").send_keys(al_num[4])
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/div").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()
        # self.driver.find_element_by_id("deletebtn").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result = "不能删除下发已经生效的灰名单"
        self.assertEqual(fact_result, expect_result)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_current_user_push_delete_f(self):
        u"电信角色ct_operator选择系统添加的wei下发状态删除"
        data_0 = self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname, pwd)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[2]").click()

        al_num = getmysql("""
                     SELECT
                             calling_number,create_time,update_time
                         FROM
                             t_greylist
                         WHERE
                              creator_type =6
                             AND ca_status=1
                             and (ct_deliver_status=1
                              or cr_deliver_status=1
                              or cm_deliver_status=1
                              or cu_deliver_status=1)
                         ORDER BY
                             greylist_id
             """)
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div[2]/div[2]/div/input").send_keys(al_num[4])
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/div").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/div").click()

        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_partial_link_text("确定").click()
        time.sleep(3)
        fact_result = self.driver.find_element_by_css_selector(".layui-layer-content").text
        expect_result = "不能删除下发已经生效的灰名单"
        self.assertEqual(fact_result, expect_result)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    #待推送
        #-----------------------2.选中多个删除
    def test_moreDel(self):
        data_0=self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname,pwd)
        u =[2,3,4]
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[%s]/td[1]/div/div/i" % u[0]).click()
        self.driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[%s]/td/div/div/i" %u[1]).click()
        self.driver.find_element_by_xpath("//div[3]/div[2]/table/tbody/tr[%s]/td/div/div/i" %u[2]).click()

        div = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div").text
        div_data = div.split('\n')
        delete_num_0 = div_data[6 * u[0] + 2]
        delete_num_1 = div_data[6 * u[1] + 2]
        delete_num_2 = div_data[6 * u[2] + 2]

        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()

        self.driver.find_element_by_link_text(u"确定").click()
        time.sleep(2)
        fact_result=self.driver.find_element_by_css_selector(".layui-layer-content").text
        print(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"删除成功"
        realDeltrue = getTrueOrFalse("""
                              SELECT
                                    calling_number,
                                    create_time,
                                    update_time
                                FROM
                                    t_greylist
                                WHERE
                                    calling_number = %s
                                OR calling_number = %s
                                OR calling_number = %s
                       """ %(delete_num_0,delete_num_1,delete_num_2))
        self.assertTrue(realDeltrue)
        self.assertEqual(fact_result,respect_result)

        #-----------------------3.选中单挑删除(分页30页第一页的任意一条
    def test_Anyone(self):
        data_0=self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname,pwd)
        u=8
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/table/tbody/tr[%s]/td[1]/div/div/i" %u).click()
        div=self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div").text
        div_data=div.split('\n')
        delete_num = div_data[6*u+2]
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_link_text(u"确定").click()
        time.sleep(3)
        fact_result=self.driver.find_element_by_css_selector(".layui-layer-content").text
        print(fact_result)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        respect_result = u"删除成功"
        # self.assertEqual(fact_result,respect_result)
        time.sleep(3)
        realDeltrue = getTrueOrFalse("""
                       select calling_number from t_greylist where calling_number=%s
               """  %delete_num)
        self.assertTrue(realDeltrue)
        print(fact_result, realDeltrue)

        #--------------------4直接点击删除按钮,提示请选中数据
    def test_DirectHits(self):
        data_0=self.data[0]
        uname = data_0['username']
        pwd = data_0["password"]
        self.greynum_delete(uname,pwd)
        time.sleep(5)
        # self.driver.find_element_by_id("deletebtn").click()
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/button[2]/i").click()
        fact_result =self.driver.find_element_by_class_name("layui-layer-content").text
        print(fact_result)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

        respect_result = u"请选择要删除的行"
        self.assertEqual(fact_result,respect_result)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
#
if __name__ == "__main__":
    box = unittest.TestSuite()
    box.addTest(GreynumDelete("test_pageallDel"))
    box.addTest(GreynumDelete("test_moreDel"))
    box.addTest(GreynumDelete("test_Anyone"))
    box.addTest(GreynumDelete("test_DirectHits"))

    with open("DeleteGreyNum.html","wb") as f :
        runner=HTMLTestRunner.HTMLTestRunner (
        stream = f,
        title = u"FZweb3_1灰名单录入delete自动化测试测试",
        description = u"测试报告",
        tester="qiwei.ren"
        )
        runner.run(box)

