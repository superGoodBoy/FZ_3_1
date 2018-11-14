#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
import  CINTEL_FZWEB3_1_2_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
import unittest
import requests
from CINTEL_FZWEB3_1_2_1.common.getfile_data_time_levelup import *
from CINTEL_FZWEB3_1_2_1.common.mysql import *
from CINTEL_FZWEB3_1_2_1.common.cut_Precise_picture import *

dbconfig={
        'host':'192.168.2.87',
        'port':3306,
        'db':'rg_web3_1',
        'user':'root',
        'passwd':'123456',
        'charset':'utf8'
    }
    
class Inter_interface(unittest.TestCase):
    def setUp(self):
        pass
    def test_top10_area(self):
        url = 'http://192.168.2.87:8080/rg_web/factRegionInterceptController/showIntercept0.shtml?starttime="2017-04-04"&endtime="2017-04-04"'
        cookie = {
            'JSESSIONID': '71efd348-438b-4196-8845-05a747aabd26;',
            ' rememberMe': 'kfZZxXLsRFhlT1EQUf+tNt35e3h1n5U2vgbyCcmnm4qdki0CGCI3K+TsuFTLiYz++HUnXXgG0xCrlKV5KHZgTPge7xb4Y/Y2dTYVQaYMmuoWOLJXyjgJPhtt1eWNEQXk/Tosd9EIpIO4va5vfb8MFYpFx8EZdo6q3t9e3c/MCY7IDscR25wAIU3558lqelMVUIQ+kWoIg/HH+qGe7uWFnOyY73yxT/3m+glJTWp1VLBo2cdMdd+92xpYjKeV6B4m9zdwSZB1fanhO9uAJiqVdmKANQ50Bbn5vBbzZkTWlNkOr+eRvFUB8ZDjVR49H2r6sasQpiJyt7XVMRcVd5hPcQ2JrPmLRfQ6XpWF2Inin71OUSOzaVfzcu/NKo9Sh2IGRaOMi8B72OLArXW2/PJA5vpQh/1aWOdKfhEmpa0fC464mc27b2/CRP0d9AcztiiBJbQFRc',
            '+JbDCfJ/q2FXgwYgxjnTLsxsuH1aNp2zrEXDs=': ''
        }
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        files = {
            'name': '全部',
            'starttime': "2017-04-04",
            'endtime': "2017-04-04",
        }
        db=Mysql(dbconfig)
        ct_operator_value = db.query("""
                                          (
                                    SELECT
                                        sum(fri.intercept_count_today)
                                    VALUE
                                        ,
                                        drd.reg_dim_id NAME,drd.province_name
                                    FROM
                                        dim_date dd
                                    LEFT JOIN fact_region_intercept fri ON dd.date_dim_id = fri.date_dim_id
                                    LEFT JOIN dim_region_district drd ON drd.reg_dim_id = fri.reg_dim_id
                                    AND fri.reg_dim_id != '0086'
                                    WHERE
                                        1 = 1
                                    AND dd.day_caption >= "2017-04-04"
                                    AND dd.day_caption <= "2017-04-04"
                                    AND drd.city_name != "invalid"
                                    AND fri.domain = 0  							
                                    GROUP BY
                                        city_name
                                    ORDER BY
                                        sum(fri.intercept_count_today) DESC
                                )
                                LIMIT 10;""")
        cm_operator_value = db.query("""(
                                         SELECT
                                             sum(fri.intercept_count_today)
                                         VALUE
                                             ,
                                             drd.reg_dim_id NAME,drd.province_name
                                         FROM
                                             dim_date dd
                                         LEFT JOIN fact_region_intercept fri ON dd.date_dim_id = fri.date_dim_id
                                         LEFT JOIN dim_region_district drd ON drd.reg_dim_id = fri.reg_dim_id
                                         AND fri.reg_dim_id != '0086'
                                         WHERE
                                             1 = 1
                                         AND dd.day_caption >= "2017-04-04"
                                         AND dd.day_caption <= "2017-04-04"
                                         AND drd.city_name != "invalid"
                                         AND fri.domain = 1  							
                                         GROUP BY
                                             city_name
                                         ORDER BY
                                             sum(fri.intercept_count_today) DESC
                                     )
                                     LIMIT 10;""")
        cu_operator_value = db.query("""
                                               (
                                         SELECT
                                             sum(fri.intercept_count_today)
                                         VALUE
                                             ,
                                             drd.reg_dim_id NAME,drd.province_name
                                         FROM
                                             dim_date dd
                                         LEFT JOIN fact_region_intercept fri ON dd.date_dim_id = fri.date_dim_id
                                         LEFT JOIN dim_region_district drd ON drd.reg_dim_id = fri.reg_dim_id
                                         AND fri.reg_dim_id != '0086'
                                         WHERE
                                             1 = 1
                                         AND dd.day_caption >= "2017-04-04"
                                         AND dd.day_caption <= "2017-04-04"
                                         AND drd.city_name != "invalid"
                                         AND fri.domain = 2						
                                         GROUP BY
                                             city_name
                                         ORDER BY
                                             sum(fri.intercept_count_today) DESC
                                     )
                                     LIMIT 10;
                                                                 """)
        cr_operator_value = db.query("""
                                               (
                                         SELECT
                                             sum(fri.intercept_count_today)
                                         VALUE
                                             ,
                                             drd.reg_dim_id NAME,drd.province_name
                                         FROM
                                             dim_date dd
                                         LEFT JOIN fact_region_intercept fri ON dd.date_dim_id = fri.date_dim_id
                                         LEFT JOIN dim_region_district drd ON drd.reg_dim_id = fri.reg_dim_id
                                         AND fri.reg_dim_id != '0086'
                                         WHERE
                                             1 = 1
                                         AND dd.day_caption >= "2017-04-04"
                                         AND dd.day_caption <= "2017-04-04"
                                         AND drd.city_name != "invalid"
                                         AND fri.domain = 3 							
                                         GROUP BY
                                             city_name
                                         ORDER BY
                                             sum(fri.intercept_count_today) DESC
                                     )
                                     LIMIT 10;
                                                                 """)
        db.close()

        # 使用requests 的post方法提交数据
        response = requests.post(url, data=files, headers=headers, cookies=cookie, allow_redirects=True)
        self.assertEqual(response.status_code,200)
        # print("电信:",sorted(ct_operator_value[00].iteritems(), key=lambda d:d[1], reverse = False ))
        # print("移动:",sorted(cm_operator_value[00].iteritems(), key=lambda d:d[1], reverse = False ))
        # print("联通:",sorted(cu_operator_value[00].iteritems(), key=lambda d:d[1], reverse = False ))
        # print("铁通:",sorted(cr_operator_value[00].iteritems(), key=lambda d:d[1], reverse = False ))
        print("电信:",ct_operator_value[00])
        print("移动:",cm_operator_value[00])
        print("联通:",cu_operator_value[00])
        if cr_operator_value.__len__() == 0:
            print("铁通没有数据")
        else:
            print("铁通:",cr_operator_value[00])
        html = response.text
        print("接口传回的运营商，及全部数据："+html)

    def test_4operator(self):
        url='http://192.168.2.87:8080/rg_web/factRegionInterceptController/showIntercept00.shtml'
        cookie= {

            'JSESSIONID':'71efd348-438b-4196-8845-05a747aabd26',
            'rememberMe':'kfZZxXLsRFhlT1EQUf+tNt35e3h1n5U2vgbyCcmnm4qdki0CGCI3K+TsuFTLiYz++HUnXXgG0xCrlKV5KHZgTPge7xb4Y/Y2dTYVQaYMmuoWOLJXyjgJPhtt1eWNEQXk/Tosd9EIpIO4va5vfb8MFYpFx8EZdo6q3t9e3c/MCY7IDscR25wAIU3558lqelMVUIQ+kWoIg/HH+qGe7uWFnOyY73yxT/3m+glJTWp1VLBo2cdMdd+92xpYjKeV6B4m9zdwSZB1fanhO9uAJiqVdmKANQ50Bbn5vBbzZkTWlNkOr+eRvFUB8ZDjVR49H2r6sasQpiJyt7XVMRcVd5hPcQ2JrPmLRfQ6XpWF2Inin71OUSOzaVfzcu/NKo9Sh2IGRaOMi8B72OLArXW2/PJA5vpQh/1aWOdKfhEmpa0fC464mc27b2/CRP0d9AcztiiBJbQFRc',
            'JbDCfJ/q2FXgwYgxjnTLsxsuH1aNp2zrEXDs':''

        }
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        files = {
            'name': '全部',
            'starttime': '2017-04-04',
            'endtime': '2018-04-04',
        }
        response=requests.post(url,cookies=cookie,headers=headers,files=files,allow_redirects=True)
        self.assertEqual(response.status_code,200)
        print(response.text)
        import json
        operator_response =json.loads(response.text)
        operator_response['world']
        db=Mysql(dbconfig)
        operator_value_total=db.query("""
        select sum(intercept_count_today), fri.domain from fact_region_intercept fri where fri.date_dim_id>=1189 and fri.date_dim_id<=1554 GROUP BY domain;
        """)
        operator_value = json.loads(response.text)['world']
        if operator_value[0]['name'] == '电信':
            ct_operator_value = operator_value[0]['value']
        elif operator_value[1]['name'] == '移动':
            cm_operator_value = operator_value[1]['value']
        elif operator_value[2]['name'] == '联通':
            cu_operator_value = operator_value[2]['value']
        elif operator_value[3]['name'] == '铁通':
            if operator_value[3]['value'] == 0:
                cr_operator_value = 0
            else:
                cr_operator_value=operator_value[3]['value']




        import json
        operator_value =json.loads(response.text)['world']
        if operator_value_total[0]['name0'] == 0:
            self.assertEquals(operator_value_total[0]['value0'], ct_operator_value)
            self.assertE
        elif operator_value_total[0]['name1'] ==1:
            self.assertEqual(operator_value_total[1]['value1'], cm_operator_value)
        elif operator_value_total[0]['name2']==2:
            self.assertEqual(operator_value_total[2]['value2'], cu_operator_value)
        else:
            if operator_value_total[0]['name3'] == None:
                operator_value_total[0]['value3'] =0
                self.assertEqual(operator_value_total[0]['value3'], cr_operator_value)
            else :
                self.assertEqual(operator_value_total[0]['value3'], cr_operator_value)


        # json[1]


# # if __name__ == 'Overseas_fraudulent_telephone_source_distribution_interface':
# if __name__ == '__main__':
#
#     reporter_dir=r's.html'
#     re_open=open(reporter_dir,'wb')
#     suite=unittest.TestLoader().loadTestsFromTestCase(Inter_interface)
#     runner =HTMLTestRunner.HTMLTestRunner(
#         stream=re_open,
#         title="FZweb3.1.2防范态势境外拦截数据",
#         description='测试情况',
#     )
#     runner.run(suite)