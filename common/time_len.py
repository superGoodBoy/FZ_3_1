#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
"""测量每个小模块的执行时间，优化执行速度"""
import time,functools
def timeit(func):
    @functools.wraps(func)
    def wrapper():
        start=time.clock()
        func()
        end = time.clock()
        print("user:",end-start)
        return wrapper()

