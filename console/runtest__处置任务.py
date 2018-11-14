#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 10:37
# @Author  : QiWei.Ren
# @Site    : 
# @File    : runtest.py
# @Software: PyCharm

import time,os,unittest
import CINTEL_FZweb3_1_1.HTMLTestRunner.HTMLTestReportEN as HTMLTestRunner
'''
# 测试用例路径:test_dir;
# 测试报告生成路径：test_report
# 测试报告标题：title
# 测试用例文件： pattern
# 设置测试人员：tester
'''
test_dir = r'F:\python_work\CINTEL_FZweb3_1_1\case\Authority_case\calling_whitelist'
# F:\python_work\CINTEL_FZweb3_1_1\HTMLTestRunner
test_report = 'F:\\python_work\\CINTEL_FZweb3_1_1\\HTMLTestRunner\\'
test_discover = unittest.defaultTestLoader.discover(test_dir, pattern='Reporter_*.py')

if __name__ == '__main__':
    name=['处置任务','综合研判','防范态势','综合查询','报表统计','基础数据','部省协同联动','公安协同联动','策略开关','权限管理','系统管理']
    dir_name=['主叫白名单下发','主叫白名单录入']
    now = time.strftime("%Y-%m-%d-%H_%M_%S")
    filename = test_report+now+name[0]+dir_name[1]+'result.html'
    print(filename)
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp, title=u'基础数据测试报告', description=u'用例执行情况:',tester='QIWEI.REN'
        )
        runner.run(test_discover)

