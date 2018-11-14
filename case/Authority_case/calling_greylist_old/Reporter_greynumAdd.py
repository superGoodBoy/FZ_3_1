#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 19:57
# @Author  : Qiwei.Ren
# @Site    : 
# @File    : Reporter_greynumAdd.py
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 13:38
# @Author  : Qiwei.Ren
# @Site    :
# @File    : addgrey_connect_mysql.py
# @Software: PyCharm
import  time
from selenium import webdriver
import unittest
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
# from CINTEL_FZweb3_1_1.tote_box.grid_module import grid_2

class GreyNumAdd(unittest.TestCase):
    def setUp(self):
    #     for host, browser in grid_2().items():
    #         driver = webdriver.Remote(
    #             command_executor=host,
    #             desired_capabilities={
    #                 'platform': 'ANY',
    #                 'browserName': browser,
    #                 'version': '',
    #                 'javascriptEnabled': True
    #             }
    #         )
        self.data =[
            {"addgreynum":"","addgreyreason":""},                                                                   #提示请输入手机号0
            {"addgreynum":"18511318433","addgreyreason":""},                                                      #提示请输入加灰原因1
            {"addgreynum":"18511318433","addgreyreason":"rqw"},                                                   #验证号码已存在2
            {"addgreynum":"#@$$$","addgreyreason":"rqw"},                                                          #输入特殊字符,提示请输入1-30手机号码3
            {"addgreynum":"1862382322","addgreyreason":"#@#4#@#@￥@￥@￥@%#%#￥sfaf#@#4#@#@￥@￥@￥@%#%#￥sfaf%#@#4#@#@￥@￥@￥@%#%#￥sfaf%%"},                        #输入特殊字符 加灰原因4添加失败
            {"addgreynum":"186238232218623823221862382322186238232218623823221862382322","addgreyreason":"234242"},          #最长手机号码校验5
            {"addgreynum":"18511318322","addgreyreason":"186238232218623823221862382322186238232218623823221862382322"},    #最长加灰校验6
            {"addgreynum":"0102432642","addgreyreason":"rqw"},
        ]
        self.driver = webdriver.Chrome()
        self.driver.get("http:\\192.168.2.87:8081/rg_web")
    def add(self,addgreynum,addgreyreason):
        self.driver.find_element_by_id("login_name").send_keys("ct_operator")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        self.driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='taskOrder']/div/div/i").click()
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        self.driver.find_element_by_xpath("//button[@onclick='addGreyList()']").click()
        self.driver.find_element_by_xpath("(//input[@name='calling_number'])[2]").send_keys(addgreynum)
        self.driver.find_element_by_name("remark").send_keys(addgreyreason)
        self.driver.find_element_by_link_text(u"保存").click()

    def test_addnum_empty(self):
        u"不输入手机号码提示:"
        data_1=self.data[0]
        print(data_1)
        addgreynum = data_1['addgreynum']
        addgreyreason = data_1['addgreyreason']
        self.add(addgreynum,addgreyreason)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_result =self.driver.execute_script("return arguments[0].textContent", demo_div)
        print(fact_result)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"必填项不能为空"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_addreason_empty(self):
        u"不输入加灰原因提示"
        data_0=self.data[1]
        print(data_0)
        addgreynum = data_0['addgreynum']
        addgreyreason = data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        demo_div = self.driver.find_element_by_id("layui-layer2")
        fact_result =self.driver.execute_script("return arguments[0].textContent", demo_div)
        print(fact_result)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"必填项不能为空"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_addnum_exists(self):
        u"已存在号码测试"
        data_0=self.data[2]
        print(data_0)
        addgreynum = data_0['addgreynum']
        addgreyreason = data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        time.sleep(3)
        demo_div = self.driver.find_element_by_class_name("layui-layer-content")
        fact_result =self.driver.execute_script("return arguments[0].textContent",demo_div)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"灰名单已经存在"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_mustbenum(self):
        u"特殊字符号码提示"
        data_0=self.data[3]
        print(data_0)
        addgreynum = data_0['addgreynum']
        addgreyreason = data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        fact_result=self.driver.find_element_by_css_selector("html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        print(fact_result)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"请输入号码1到30位数字"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)


    def test_china_reason(self):

        data_0=self.data[4]
        print(data_0)
        time.sleep(3)
        addgreynum = data_0['addgreynum']
        addgreyreason = data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        time.sleep(1)
        fact_result=self.driver.find_element_by_css_selector(
            "html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg"
        ).text
        print(fact_result)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"输入原因不能为空且在50字符 以内 ！"
        self.assertEqual(except_result ,fact_result)

    def test_not_toolong_num(self):
        u"加灰号码输入特长 提示"
        data_0=self.data[5]
        print(data_0)
        addgreynum = data_0['addgreynum']
        addgreyreason = data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        fact_result=self.driver.find_element_by_css_selector("html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        print(fact_result)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"请输入号码1到30位数字"
        print(fact_result, except_result)
        self.assertEqual(except_result ,fact_result)

    def test_not_toolong_reason(self):
        u"加灰原因输入特长 提示"
        data_0=self.data[6]
        print(data_0)
        addgreynum = data_0['addgreynum']
        addgreyreason = data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        fact_result=self.driver.find_element_by_css_selector("html body div#layui-layer2.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        except_result = u"输入原因不能为空且在50字符 以内 ！"
        print(fact_result,except_result)
        self.assertEqual(except_result ,fact_result)

    def test_addgreynum_success(self):
        u"验证成功添加用例"
        data_0=self.data[7]
        print(data_0)
        addgreynum = data_0['addgreynum']
        addgreyreason =data_0['addgreyreason']
        self.add(addgreynum,addgreyreason)
        time.sleep(3)
        fact_result=self.driver.find_element_by_xpath("//*[@id='layui-layer2']/div").text
        print(fact_result)
        except_result=u"添加成功"
        print(fact_result, except_result)
        self.assertEqual(except_result,fact_result)

    def tearDown(self):
        self.driver.quit()
if __name__ == '__main__':

    box = unittest.TestSuite()
    box.addTest(GreyNumAdd("test_addnum_empty"))
    box.addTest(GreyNumAdd("test_addreason_empty"))
    box.addTest(GreyNumAdd("test_addnum_exists"))
    box.addTest(GreyNumAdd("test_mustbenum"))
    box.addTest(GreyNumAdd("test_china_reason"))
    box.addTest(GreyNumAdd("test_not_toolong_reason"))
    box.addTest(GreyNumAdd("test_not_toolong_num"))
    box.addTest(GreyNumAdd("test_addgreynum_success"))
    #return box
    with open("AddGreyNum.html","wb") as f :
        runner=HTMLTestRunner.HTMLTestRunner (
        stream = f,
        title = u"FZweb3_1灰名单录入add功能测试",
        description = u"测试报告",
        tester="QIWEI.REN"
        )
        runner.run(box)
