#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 10:56
# @Author  : QiWei.Ren
# @Site    : 
# @File    : log.py
# @Software: PyCharm
import os,time,logging

log_path = r"F:\CINTEL_FZweb3_1_2\CINTEL_FZWEB3_1_2_1\logger" #日志文件路径
class Log:
    def __init__(self):
        self.logname=os.path.join(log_path,'%s.log' %time.strftime("%Y_%m_%d_%H_%M_%S"))
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter=logging.Formatter('[%(asctime)s]-%(filename)s[line:%(lineno)d]-fuc:%(funcName)s-%(levelname)s:%(message)s')

    def __console(self,level,message):
        fh =logging.FileHandler(self.logname,'a')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level =="debug":
            self.logger.debug(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)

        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()

    def debug(self, message):
        self.__console('debug',message)

    def error(self, message):
        self.__console('error',message)

    def warning(self, message):
        self.__console('warning',message)

    def info(self, message):
        self.__console('info',message)

if __name__ == '__main__':
    log =Log()
    log.info(u'-测试开始-')
    log.info(u'-输入密码-')
    log.info(u'-测试结束-')
