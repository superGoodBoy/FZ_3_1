#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# from .mysql import Mysql
"""
获取参数　ｕｒｌ，然后将ｕｒｌ传入到ｃａｓｅ　用例中，修改未完成
"""

from CINTEL_FZWEB3_1_2_1.common.mysql import Mysql
dbconfig = {
    'host': 'localhost',
    'port': 3306,
    'db': 'rg_web3_1',
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8'
}
db=Mysql(dbconfig)
url=db.select('visit_url','url')
print(url)
db.close()
