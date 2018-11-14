#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren

import pymysql
import time
"""
realdelete or not
判断识别web是否真删
"""
def getTrueOrFalse(sql):
    con = pymysql.connect("192.168.2.63","root","123456", "rg_web3_1")
    with con:
        cursor = con.cursor()
        calling_number=cursor.execute(sql)
        print(calling_number)
        if calling_number !=0:
            return False
            print("数据库内删除失败")
        else:
            return True
            print("数据库内已删除成功")

"""
封装mysql：增删改查
"""
class Mysql(object):
    def __init__(self, dbconfig: object) -> object:
        self.host = dbconfig['host']
        self.port = dbconfig['port']
        self.dbname=dbconfig['db']
        self.user = dbconfig['user']
        self.password = dbconfig['passwd']
        self.charset=dbconfig['charset']
        self._conn=None
        self._connect()
        self._cursor=self._conn.cursor()

    def _connect(self):
        """链接数据库"""
        try:
            self._conn=pymysql.connect(host=self.host,port=self.port,db=self.dbname,user=self.user,passwd=self.password,charset=self.charset)
        except pymysql.Error as e:
            print(e)
    def query(self,sql):
        """查询抛异常"""
        try:
            result = self._cursor.execute(sql)
        except pymysql.Error as e:
            print(e)
            result=False
        return result
    def select(self,table,colume="",condition=''):
        """查询是否有where限制 条件"""
        condition ='where ' +condition if condition else None
        if condition:
            sql = "select %s from %s %s" % (colume, table, condition)
            # sql= "select %s from %s %s"%(colume,table,condition)
        else:
            sql="select %s from %s"%(colume,table)
        self.query(sql)
        return  self._cursor.fetchall()
    def insert(self,table,tdict):
        colume=''
        value=''
        for key in tdict:
            colume += ','+key
            # value += "','" +tdict['key']
            value += "','" + tdict[key]
        colume=colume[1:]
        value = value[2:]+"'"
        sql = "insert into %s(%s) value (%s)" %(table,colume,value)
        self._cursor.execute(sql)
        self._conn.commit()
        return self._cursor.lastrowid  #返回最后的id
    def update(self,table,tdict,condition=''):
        if not condition:
            print("must hava id")
            exit()
        else:
            condition = "where " +condition
        value=''
        for key in tdict:
            value += "%s = %s"%(key,tdict[key])
        sql="update %s set %s %s"%(table,value,condition)
        self._cursor.execute(sql)
        return self.affected_num() #返回影响的行数
    def delete(self,table,condition=''):
        condition = "where "+ condition if condition else None
        sql="delete from %s %s" %(table,condition)
        print(sql)
        self._cursor.execute(sql)
        self._conn.commit()
        return self.affected_num()
    def rollback(self):
        self._conn.rollback()
    def affected_num(self):
        return self._cursor.rowcount

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.close()
        except:
            pass

    def make_list(t):
        """元组转换list"""
        l = []
        for e in t:
            l.append(e[0])
        return l

    def close(self):
        self.__del__()

if __name__ == '__main__':
    dbconfig={
        'host':'192.168.2.87',
        'port':3306,
        'db':'rg_web3_1',
        'user':'root',
        'passwd':'123456',
        'charset':'utf8'
    }
    db=Mysql(dbconfig)
    tdict={
        'whitelist_id':'1833333225333',
        'calling_number':'1822222'
    }

    # print(db.insert(table='t_whitelist',tdict=tdict))
    # tdict={
    #     'list_type':3
    # }
    # print(db.delete(table='t_whitelist',condition='calling_number=13320934118'))
    # print(db.update(table='t_whitelist',tdict=tdict,condition='calling_number=13320934118'))
    # print(db.select(table='t_whitelist',colume='calling_number',condition='list_type=2'))

    db.close()