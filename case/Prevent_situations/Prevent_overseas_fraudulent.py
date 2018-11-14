#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import unittest,time
from PIL import Image
import pytesseract as rec
import pymysql as mdb
from selenium import webdriver
from CINTEL_FZWEB3_1_2_1.logger.log import *
import CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.cut_Precise_picture import *

rec.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract'
def verify(picturename):
    img = Image.open(picturename)
    code = rec.image_to_string(img)
    return code
start_tim=time.strftime("%Y-%m-%d")
log=Log()
dbconfig = {
            'host': '192.168.2.87',
            'port': 3306,
            'db': 'rg_web3_1',
            'user': 'root',
            'passwd': '123456',
            'charset': 'utf8'
        }
class Inter_interface(unittest.TestCase):
    def setUp(self):
        self.driver=webdriver.PhantomJS()
        # self.driver=webdriver.Chrome()
        log.info("打开浏览器")
        # self.driver.maximize_window()
        self.driver.set_window_size(1200, 900)
        self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.2.87:8080/rg_web/")

    def tearDown(self):
        log.info("关闭浏览器")
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.find_element_by_id("login_name").send_keys('ct_operator')
        time.sleep(2)
        driver.find_element_by_id("password").send_keys('123456')
        self.driver.find_element_by_xpath("//*[@id='vcode']").send_keys("8888")
        driver.find_element_by_xpath("//div[@onclick='loginSubmit()']").click()
        self.driver.implicitly_wait(30)
        log.info("%s用户，登录成功" % self.driver.find_element_by_class_name("protel").text[1:])
        driver.find_element_by_css_selector(
            "#situationAnalysis>div.swiper-slide.icon-h-w.swiper-slide-active>div").click()
        self.driver.implicitly_wait(30)
        log.info(self.driver.find_element_by_class_name("layui-layer-title").text)
        driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe"))

    def test_top10_area(self):
        driver = self.driver
        self.login()
        time.sleep(5)
        his_time='2015-05-17'
        now_time=start_tim
        js='document.getElementById("Time").value="%s - %s"'%(his_time,now_time)
        driver.execute_script(js)
        js1='document.getElementById("jw_tab1").click()'   #全部　
        driver.execute_script(js1)
        time.sleep(20)
        driver.get_screenshot_as_file(r'F:\python_work\CINTEL_FZweb3_1_1\case\Prevent_situations\result\2_2_top10.jpg')
        file_path = r"F:\python_work\CINTEL_FZweb3_1_1\case\Prevent_situations\result\2_2_top10.jpg"
        image = Image.open(file_path)
        print(image.size)
        image_list = cut_image_operator(image, box=(566, 365, 1050, 720))
        save_images(image_list, index="国外拦截top10.jpg")

        sql="""
                        (
                SELECT
                    sum(fri.intercept_count_today)
                VALUE
                    ,
                    drd.reg_dim_id CODE,
                    drd.city_name NAME
                FROM
                    dim_date d
                LEFT JOIN fact_region_intercept fri ON d.date_dim_id = fri.date_dim_id
                LEFT JOIN dim_region_district drd ON drd.reg_dim_id = fri.reg_dim_id
                AND d.day_caption > '%s'
                AND d.day_caption < '%s'
                AND drd.city_name != 'invalid'
                GROUP BY
                    drd.city_name
                ORDER BY
                    sum(fri.intercept_count_today) DESC
            )
            LIMIT 10
        """%(his_time,start_tim)
        db = Mysql(dbconfig)
        m=db.highquery(sql)
        db.close()
        log.debug(m)

    def test_operator(self):
        driver=self.driver
        self.login()
        time.sleep(5)
        his_time = '2015-05-17'
        now_time = start_tim
        js = 'document.getElementById("Time").value="%s - %s"' % (his_time, now_time)
        driver.execute_script(js)
        js1 = 'document.getElementById("jw_tab1").click()'  # 全部　
        driver.execute_script(js1)
        time.sleep(20)
        driver.get_screenshot_as_file(
            r'F:\python_work\CINTEL_FZweb3_1_1\case\Prevent_situations\result\2_2_operator.jpg')
        file_path = r"F:\python_work\CINTEL_FZweb3_1_1\case\Prevent_situations\result\2_2_operator.jpg"
        image = Image.open(file_path)
        print(image.size)
        image_list = cut_image_operator(image, box=(600, 161, 737, 260))
        save_images(image_list, index="国外拦截电信总拦截数.jpg")

        sql = """
                 select fri.domain name,sum(intercept_count_today) value from fact_region_intercept fri
                    left join dim_date dd on  fri.date_dim_id=dd.date_dim_id where 1=1
                and dd.day_caption >="%s"
                and dd.day_caption <="%s"
                and fri.is_inland =0
                GROUP BY domain order by sum(intercept_count_today) asc;
               """%(his_time,start_tim)
        db = Mysql(dbconfig)
        m = db.highquery(sql)
        db.close()
        log.debug(m)

