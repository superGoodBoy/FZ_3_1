#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 13:32
# @Author  : QiWei.Ren
# @Site    : 
# @File    : highselect_getmysql.py
# @Software: PyCharm
"""
返回号码列表　　此模块可追入　．／ｍｙｓｑｌ文件夹
"""
import pymysql as mdb
def getmysql(sql):
    con = mdb.connect("192.168.2.63", "root", "123456", "rg_web3_1")
    with con:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        mysql_list = []
        for row in list(rows):
            # print(list(row))
            row = list(row)[0]
            mysql_list.append(row)
        mysql_list.sort()

    return mysql_list