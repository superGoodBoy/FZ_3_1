#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from CINTEL_FZWEB3_1_2_1.logger.log import *
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

log=Log()
class User_add(unittest.TestCase):
    def setUp(self):
        log.info("打开浏览器")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml;JSESSIONID=64cfb342-47f2-4404-8339-bf47d4913c2f")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()
        self.assertEqual([], self.verificationErrors)

    def login(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys("itim")
        driver.find_element_by_id("password").send_keys("itim204")
        driver.find_element_by_id("vcode").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])

        click_btn = self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('yhgl')\"]")
        action = ActionChains(self.driver)
        write = self.driver.find_element_by_xpath("//i[@onclick=\"appFunction('yhgl')\"]")
        action.move_to_element(write).perform()
        click_btn.click()

        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        time.sleep(5)

    def test_addpart_nameempty(self):
        """添加部门"""
        self.login()
        self.driver.find_element_by_id("add-department").click()
        self.driver.find_element_by_xpath("//input[@value='']").click()
        self.driver.find_element_by_xpath("//form[@id='saveDept']/div/div/div/div/dl/dd[2]").click()
        self.driver.find_element_by_name("dept_name").click()
        self.driver.find_element_by_name("dept_name").clear()
        self.driver.find_element_by_name("dept_name").send_keys("")

        self.driver.find_element_by_id("saveDept1").click()
        time.sleep(1)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name =self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name="必填项不能为空"
        self.assertEqual(fact_name,expe_name)
        self.driver.find_element_by_xpath("/html/body/div[3]/span[1]/a[3]").click()

    def test_addpart_success(self):
        driver = self.driver
        self.login()
        driver.find_element_by_id("add-department").click()
        driver.find_element_by_xpath("//input[@value='']").click()
        driver.find_element_by_xpath("//form[@id='saveDept']/div/div/div/div/dl/dd[2]").click()
        driver.find_element_by_name("dept_name").click()
        driver.find_element_by_name("dept_name").clear()
        driver.find_element_by_name("dept_name").send_keys("反炸总部")
        self.driver.find_element_by_id("saveDept1").click()

        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "添加成功"
        self.assertEqual(fact_name, expe_name)
        self.driver.find_element_by_xpath("/html/body/div[3]/span[1]/a[3]").click()

    def test_addpart_exits(self):
        driver = self.driver
        self.login()
        driver.find_element_by_id("add-department").click()
        driver.find_element_by_xpath("//input[@value='']").click()
        driver.find_element_by_xpath("//form[@id='saveDept']/div/div/div/div/dl/dd[2]").click()
        driver.find_element_by_name("dept_name").send_keys("反炸总部")
        self.driver.find_element_by_id("saveDept1").click()

        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "部门已存在，请勿重复添加"
        self.assertEqual(fact_name, expe_name)
        self.driver.find_element_by_xpath("/html/body/div[3]/span[1]/a[3]").click()

    def test_delPart_existUser(self):
        self.login()
        # self.driver.find_element_by_xpath("//*[@id='tree']/ul/li[2]").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/button[1]/i").click()
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "不可删除，此部门下有员工"
        self.assertEqual(fact_name, expe_name)

        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/button[3]/i").click()

    def test_delPart_success(self):
        self.login()
        self.driver.find_element_by_xpath("//*[@id='tree']/ul/li[2]").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/button[1]/i").click()
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "删除成功"
        self.assertEqual(fact_name, expe_name)

        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/button[3]/i").click()

    def test_editPart_empty(self):
        self.login()
        # self.driver.find_element_by_xpath("//*[@id='tree']/ul/li[2]").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/button[3]/i").click()

        time.sleep(0.5)
        demo_div = self.driver.find_element_by_class_name("layui-layer-content")
        fact_name = self.driver.execute_script("return arguments[0].textContent",demo_div)
        expe_name = "请选择要修改的部门"
        self.assertEqual(fact_name, expe_name)

    def test_editPart_success(self):
        self.login()
        self.driver.find_element_by_xpath("//*[@id='tree']/ul/li[2]").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/button[3]/i").click()
        self.driver.find_element_by_id("updateDept").click()
        time.sleep(1)
        demo_div = self.driver.find_elements_by_class_name("layui-layer-content")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "删除成功"
        self.assertEqual(fact_name, expe_name)

    def test_addUser_usernameempty(self):
        """添加用户及信息"""
        self.login()
        self.driver.find_element_by_id("add").click()
        self.driver.find_element_by_id("save_username").send_keys(u"")                  #1
        self.driver.find_element_by_id("save_login_account").send_keys("rqw")           #2
        self.driver.find_element_by_xpath("(//input[@value=''])[3]").click()            #3
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[3]/div/div/div/dl/dd[5]").click()
        self.driver.find_element_by_xpath("(//input[@value=''])[4]").click()            #4
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[4]/div/div/div/dl/dd[9]").click()
        self.driver.find_element_by_id("save_email").send_keys("752737781@qq.com")      #5
        self.driver.find_element_by_id("saveUser").click()                              #6
        self.driver.find_element_by_xpath("//div[@id='save_user_carrieroperators']/div[2]/i").click() #7
        self.driver.find_element_by_id("save_phone").send_keys("18511318433")           #8
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[10]/div/button").click()
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)

    def test_addUser_loginaccount_empty(self):
        self.login()
        self.driver.find_element_by_id("add").click()
        self.driver.find_element_by_id("save_username").send_keys(u"任起伟")
        self.driver.find_element_by_id("save_login_account").send_keys("")
        self.driver.find_element_by_xpath("(//input[@value=''])[3]").click()
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[3]/div/div/div/dl/dd[5]").click()
        self.driver.find_element_by_xpath("(//input[@value=''])[4]").click()
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[4]/div/div/div/dl/dd[9]").click()
        self.driver.find_element_by_id("save_email").send_keys("752737781@qq.com")
        self.driver.find_element_by_id("saveUser").click()
        self.driver.find_element_by_xpath("//div[@id='save_user_carrieroperators']/div[2]/i").click()
        self.driver.find_element_by_id("save_phone").send_keys("18511318433")
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[10]/div/button").click()

        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "必填项不能为空"
        self.assertEqual(fact_name, expe_name)

    def test_addUser__email_empty(self):
        """添加用户及信息"""
        self.login()
        self.driver.find_element_by_id("add").click()
        self.driver.find_element_by_id("save_username").send_keys(u"任wwu")  # 1
        self.driver.find_element_by_id("save_login_account").send_keys("rqw33")  # 2
        self.driver.find_element_by_xpath("(//input[@value=''])[3]").click()  # 3
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[3]/div/div/div/dl/dd[5]").click()
        self.driver.find_element_by_xpath("(//input[@value=''])[4]").click()  # 4
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[4]/div/div/div/dl/dd[9]").click()
        self.driver.find_element_by_id("save_email").send_keys(" ")  # 5
        self.driver.find_element_by_id("saveUser").click()  # 6
        self.driver.find_element_by_xpath("//div[@id='save_user_carrieroperators']/div[2]/i").click()  # 7
        self.driver.find_element_by_id("save_phone").send_keys("18511318433")  # 8
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[10]/div/button").click()
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "邮箱格式不正确"
        self.assertEqual(fact_name, expe_name)

    def test_addUser_email_rule(self):
        """添加用户及信息"""
        self.login()
        self.driver.find_element_by_id("add").click()
        self.driver.find_element_by_id("save_username").send_keys(u"任wwu")  # 1
        self.driver.find_element_by_id("save_login_account").send_keys("rqw33")  # 2
        self.driver.find_element_by_xpath("(//input[@value=''])[3]").click()  # 3
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[3]/div/div/div/dl/dd[5]").click()
        self.driver.find_element_by_xpath("(//input[@value=''])[4]").click()  # 4
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[4]/div/div/div/dl/dd[9]").click()
        self.driver.find_element_by_id("save_email").send_keys("2344252")  # 5
        self.driver.find_element_by_id("saveUser").click()  # 6
        self.driver.find_element_by_xpath("//div[@id='save_user_carrieroperators']/div[2]/i").click()  # 7
        self.driver.find_element_by_id("save_phone").send_keys("18511318433")  # 8
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[10]/div/button").click()
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "邮箱格式不正确"
        self.assertEqual(fact_name, expe_name)

    def test_addUser_exists(self):

        """添加用户及信息"""
        self.login()
        self.driver.find_element_by_id("add").click()
        self.driver.find_element_by_id("save_username").send_keys(u"任wwu")  # 1
        self.driver.find_element_by_id("save_login_account").send_keys("rqw33")  # 2
        self.driver.find_element_by_xpath("(//input[@value=''])[3]").click()  # 3
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[3]/div/div/div/dl/dd[5]").click()
        self.driver.find_element_by_xpath("(//input[@value=''])[4]").click()  # 4
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[4]/div/div/div/dl/dd[9]").click()
        self.driver.find_element_by_id("save_email").send_keys("1@qq.com")  # 5
        self.driver.find_element_by_id("saveUser").click()  # 6
        self.driver.find_element_by_xpath("//div[@id='save_user_carrieroperators']/div[2]/i").click()  # 7
        self.driver.find_element_by_id("save_phone").send_keys("18511318433")  # 8
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[10]/div/button").click()
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "用户已存在，请勿重复添加"
        self.assertEqual(fact_name, expe_name)

    def test_addUser_success(self):
        """添加用户及信息"""
        self.login()
        self.driver.find_element_by_id("add").click()
        self.driver.find_element_by_id("save_username").send_keys(u"任wwu")  # 1
        self.driver.find_element_by_id("save_login_account").send_keys("rqw33")  # 2
        self.driver.find_element_by_xpath("(//input[@value=''])[3]").click()  # 3
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[3]/div/div/div/dl/dd[5]").click()
        self.driver.find_element_by_xpath("(//input[@value=''])[4]").click()  # 4
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[4]/div/div/div/dl/dd[9]").click()
        self.driver.find_element_by_id("save_email").send_keys("1@qq.com")  # 5
        self.driver.find_element_by_id("saveUser").click()  # 6
        self.driver.find_element_by_xpath("//div[@id='save_user_carrieroperators']/div[2]/i").click()  # 7
        self.driver.find_element_by_id("save_phone").send_keys("18511318433")  # 8
        self.driver.find_element_by_xpath("//form[@id='saveUser']/div[10]/div/button").click()
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "添加成功"
        self.assertEqual(fact_name, expe_name)

    def test_delUser_empty(self):
        self.login()

        # self.driver.find_element_by_xpath("//*[@id='list']/tr[1]/td[1]/div/i").click()
        self.driver.find_element_by_xpath("//*[@id='delete']/i").click()
        # self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        demo_div =  demo_div = self.driver.find_element_by_class_name("layui-layer-content")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "请选择需要操作的员工记录"
        self.assertEqual(fact_name, expe_name)

    def test_delUser_success(self):
        self.login()

        self.driver.find_element_by_xpath("//*[@id='list']/tr[1]/td[1]/div/i").click()
        self.driver.find_element_by_xpath("//*[@id='delete']/i").click()
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        time.sleep(1)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "删除成功"
        self.assertEqual(fact_name, expe_name)

    def test_editUser_success(self):

        self.login()
        self.driver.find_element_by_xpath("//*[@id='list']/tr[1]/td[1]/div/i").click()
        self.driver.find_element_by_xpath("//*[@id='list']/tr[1]/td[10]/button[1]").click()
        self.driver.find_element_by_id("update_username")
        self.driver.find_element_by_id("update_login_account")
        #3
        #4
        # self.driver.find_element_by_xpath("(//*[@id='updateUser']/div[3]/div/div/div/div/input").click()  # 3
        # self.driver.find_element_by_xpath("//*[@id='updateUser']/div[3]/div/div/div/dl/dd[3]").click()
        # self.driver.find_element_by_xpath("//*[@id='updateUser']/div[4]/div/div/div/div/input").click()  # 4
        # self.driver.find_element_by_xpath("//*[@id='updateUser']/div[4]/div/div/div/dl/dd[9]").click()
        #
        # self.driver.find_element_by_id("update_phone")
        # self.driver.find_element_by_id("update_email")
        #
        #
        self.driver.find_element_by_id('updateUser1').submit()
        time.sleep(0.4)
        demo_div = self.driver.find_elements_by_class_name("layui-layer-content")
        # demo_div1 = self.driver.find_elements_by_class_name("layui-layer-padding")
        css =self.driver.find_element_by_css_selector(".layui-layer-content.layui-layer-padding")
        print(demo_div,css)
        fact_name = self.driver.execute_script("return arguments[0].textContent", demo_div)
        expe_name = "删除成功"
        self.assertEqual(fact_name, expe_name)

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

if __name__ == "__main__":
    unittest.main()
