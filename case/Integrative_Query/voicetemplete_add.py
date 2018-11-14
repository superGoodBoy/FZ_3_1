#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
dbconfig = {
    'host': '192.168.2.87',
    'port': 3306,
    'db': 'rg_web3_1',
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8'
}
import unittest,xlrd
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
from selenium.webdriver.support.ui import WebDriverWait
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from selenium.webdriver.common.action_chains import ActionChains
log=Log()
class Voicetemplete(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        log.info("打开浏览器")
        self.driver.get("http://192.168.2.87:8080/rg_web/login.shtml")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        driver = self.driver
        self.driver.implicitly_wait(30)
        driver.find_element_by_id("login_name").send_keys("ca_system_admin")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("vcode").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        # --不稳定
        # click_btn = driver.find_element_by_css_selector("//*[@id='selectData']/div[4]/div")
        click_btn = driver.find_elements_by_class_name("app-title")[19]
        action = ActionChains(self.driver)
        write =driver.find_elements_by_class_name("app-title")[19]
        action.move_to_element(write).perform()
        click_btn.click()

        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))
        time.sleep(2)

    #添加用例
    def test_addfile_empty(self):
        self.login()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_css_selector("body>div.box.box-primary>div:nth-child(2)>div.row-left>div>button:nth-child(1)").click()
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_id("template_content"))
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_name("th_audio_tag"))
        # self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button").click()
        # callexe(exe_path=r"C:\Users\renqiwei\Desktop\study\exefile", exe_file='wav.exe')
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[1]/div[1]/i").click()
        self.driver.find_element_by_id("template_name").send_keys("欺骗诈骗")
        self.driver.find_element_by_id("template_content").send_keys("就骗你钱咋地")
        self.driver.find_elements_by_id("template_key")[1].send_keys('骗')
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name="请选择要上传的文件"
        self.assertEqual(fact_name,expe_name)

    def test_addbutton_empty(self):
        self.login()
        self.driver.find_element_by_css_selector("body> div.box.box-primary> div:nth-child(2)> div.row-left>div>button:nth-child(1)").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("template_content"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("th_audio_tag"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button"))
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button").click()
        time.sleep(1)
        callexe(exe_path=r"C:\Users\renqiwei\Desktop\study\exefile", exe_file='wav.exe')
        time.sleep(2)
        self.driver.implicitly_wait(30)
        # self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[1]/div[1]/i").click()
        self.driver.find_element_by_id("template_name").send_keys("欺骗诈骗 ")
        self.driver.find_element_by_id("template_content").send_keys("就骗你钱咋地")
        self.driver.find_elements_by_id("template_key")[1].send_keys('骗')
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "请选择模板标签"
        self.assertEqual(fact_name, expe_name)

    def test_addtemplate_name_empty(self):
        self.login()
        self.driver.find_element_by_css_selector("body>div.box.box-primary>div:nth-child(2)>div.row-left>div>button:nth-child(1)").click()
        self.driver.implicitly_wait(30)
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("template_content"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("th_audio_tag"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button"))
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button").click()
        time.sleep(1)
        callexe(exe_path=r"C:\Users\renqiwei\Desktop\study\exefile", exe_file='wav.exe')
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[1]/div[1]/i").click()
        self.driver.find_element_by_id("template_name").send_keys("")
        self.driver.find_element_by_id("template_content").send_keys("就骗你钱咋地")
        self.driver.find_elements_by_id("template_key")[1].send_keys('骗')
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "模板名不能为空"
        self.assertEqual(fact_name, expe_name)

    def test_addtemplate_content_empty(self):
        self.login()
        self.driver.find_element_by_css_selector("body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("template_content"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("th_audio_tag"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button"))
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button").click()
        time.sleep(1)
        callexe(exe_path=r"C:\Users\renqiwei\Desktop\study\exefile", exe_file='wav.exe')
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[1]/div[1]/i").click()
        self.driver.find_element_by_id("template_name").send_keys("就骗你钱咋地")
        self.driver.find_element_by_id("template_content").send_keys("")
        self.driver.find_elements_by_id("template_key")[1].send_keys('骗')
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "样本内容不能为空且在1000字符 以内 ！"
        self.assertEqual(fact_name, expe_name)

    def test_addtemplate_key_empty(self):
        self.login()
        self.driver.find_element_by_css_selector("body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("template_content"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("th_audio_tag"))
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button"))
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button").click()
        time.sleep(1)
        callexe(exe_path=r"C:\Users\renqiwei\Desktop\study\exefile", exe_file='wav.exe')
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[1]/div[1]/i").click()
        self.driver.find_element_by_id("template_name").send_keys("就骗你钱咋地")
        self.driver.find_element_by_id("template_content").send_keys("骗")
        self.driver.find_elements_by_id("template_key")[1].send_keys('')
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "关键字长度不能大于50，且不能为空"
        self.assertEqual(fact_name, expe_name)

    def test_add_success(self):
        self.login()
        self.driver.find_element_by_css_selector(
            "body > div.box.box-primary > div:nth-child(2) > div.row-left > div > button:nth-child(1)").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("template_content"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name("th_audio_tag"))
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button"))
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[1]/div/button").click()
        time.sleep(1)
        callexe(exe_path=r"C:\Users\renqiwei\Desktop\study\exefile", exe_file='wav.exe')
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addForm']/div[2]/div/div[1]/div[1]/i").click()
        self.driver.find_element_by_id("template_name").send_keys("AA")
        self.driver.find_element_by_id("template_content").send_keys("AA")
        self.driver.find_elements_by_id("template_key")[1].send_keys('RA')
        self.driver.find_element_by_class_name("layui-layer-btn0").click()

        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "添加成功"
        self.assertEqual(fact_name, expe_name)
    # 导出用例
    def test_export_empty(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[4]/i").click()
        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expec_name = "请选择要导出的行"
        self.assertEqual(expec_name, fact_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_export_success(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[4]/i").click()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
        time.sleep(5)
        filename = filedata_time_level01(name_title="长途区号2018年06", title_len=29, path=r"C:\Users\renqiwei\Downloads")
        print(filename)
        data = xlrd.open_workbook(r'C:\Users\renqiwei\Downloads\%s' % filename)
        table = data.sheets()[0]
        log.debug("excel文件条数：%s" % table._cell_values.__len__())

    #编辑用例
    def test_edit_success(self):
        self.login()
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div/div/div[1]/div[3]/div[2]/table/tbody/tr[1]/td/div/div/i").click()
        self.driver.find_element_by_css_selector(
            "body>div.box.box-primary>div:nth-child(2)>div.row-left>div>button:nth-child(3)").click()
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("layui-layer-btn0"))
        self.driver.find_element_by_xpath("//*[@id='updateForm']/div[1]/div/div[1]/div[2]/i").click()

        self.driver.find_element_by_id("template_name").send_keys("ras")
        self.driver.find_element_by_id("template_content").send_keys("bs")
        self.driver.find_elements_by_id("template_key")[1].send_keys("fad")
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "修改语音模板成功"
        self.assertEqual(fact_name, expe_name)
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    #删除用例
    def test_del_empty(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]/i").click()

        fact_name = self.driver.find_element_by_css_selector(
            "div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "请选择要删除的行"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_success(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]/i").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[1]/div[3]/div[2]/table/tbody/tr[1]/td/div/div/i").click()
        time.sleep(1)
        fact_name = self.driver.find_element_by_css_selector("div.layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg").text
        log.debug(fact_name)
        expe_name = "删除成功"
        self.assertEqual(fact_name, expe_name)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_del_success(self):
        self.login()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/button[2]/i").click()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()
    #查询用例
    def test_query_template_name(self):
        self.login()
        template_name="放大所无法"
        self.driver.find_element_by_name("template_name").send_keys(template_name)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]").click()
        fact_num=self.driver.find_element_by_id("totalRecord").text
        db=Mysql(dbconfig)
        expe_num=db.select(table='t_voicetemplate',colume='template_name',condition='template_name="%s" order by create_time'%template_name).__len__()
        log.debug(expe_num)
        log.debug(fact_num)
        db.close()
        self.assertEqual(fact_num,expe_num)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_template_id(self):
        self.login()
        template_name = "12956"
        self.driver.find_element_by_name("template_id").send_keys(template_name)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]").click()
        fact_num = self.driver.find_element_by_id("totalRecord").text
        db = Mysql(dbconfig)
        expe_num = db.select(table='t_voicetemplate', colume='template_id',
                             condition='template_id="%s" order by create_time' % template_name).__len__()
        log.debug(expe_num)
        log.debug(fact_num)
        db.close()
        self.assertEqual(fact_num, expe_num)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_b_template_id(self):
        self.login()
        b_template_id = "12956"
        self.driver.find_element_by_name("b_template_id").send_keys(b_template_id)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]").click()
        fact_num = self.driver.find_element_by_id("totalRecord").text
        db = Mysql(dbconfig)
        expe_num = db.select(table='t_voicetemplate', colume='b_template_id',
                             condition='b_template_id="%s" order by create_time' % b_template_id).__len__()
        log.debug(expe_num)
        log.debug(fact_num)
        db.close()
        self.assertEqual(fact_num, expe_num)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_tag(self):
        self.login()
        s_audio_tag=201
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div")
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[2]/div[4]/div/div/dl/dd[2]").click()

        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]").click()
        fact_num = self.driver.find_element_by_id("totalRecord").text
        db = Mysql(dbconfig)
        expe_num = db.select(table='t_voicetemplate', colume='b_template_id',
                             condition='s_audio_tag="%s" order by create_time' % s_audio_tag).__len__()
        log.debug("%s,%s" % (expe_num, fact_num))
        db.close()
        self.assertEqual(fact_num, expe_num)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()

    def test_query_template_key(self):
        self.login()
        template_key = "5345"
        self.driver.find_element_by_name("template_key").send_keys(template_key)
        self.driver.find_element_by_xpath("//*[@id='conditionForm']/div[1]/button[1]").click()
        fact_num = self.driver.find_element_by_id("totalRecord").text
        db = Mysql(dbconfig)
        expe_num = db.select(table='t_voicetemplate', colume='template_key',condition='template_key="%s" order by create_time' % template_key).__len__()
        log.debug("%s,%s"%(expe_num,fact_num))
        db.close()
        self.assertEqual(fact_num, expe_num)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//div[@id='layui-layer1']/span/a[2]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@onclick='togglePro()']").click()
        self.driver.find_element_by_xpath("//li[@onclick='quit()']").click()