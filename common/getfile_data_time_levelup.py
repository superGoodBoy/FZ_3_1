#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26 14:10
# @Author  : Qiwei.Ren
# @Site    : 
# @File    : getfile_num.py
# @Software: PyCharm
"""
1.获取某模块下载的excel文档
2.识别过滤其他模块文档
3.自动识别最新的下载文档
4.不识别文档内容
"""
import re,time,os,datetime,os.path,sys,xlrd,win32process, win32event
"""实现最新月份,最新年份识别"""
def newestdate():
    date={}
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    pastTime = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')  # 过去一小时时间
    afterTomorrowTime = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')  # 后天
    tomorrowTime = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')  # 明天
    # print('\n', nowTime, '\n', pastTime, '\n', afterTomorrowTime, '\n', tomorrowTime)

    nowmonth=nowTime[5:7]
    nowyear=nowTime[:4]
    date['year'] =int(nowyear)
    date['month']=(nowmonth.zfill(1))
    print(date)
    return date
if __name__ == '__main__':
    newestdate()

"""准确识别下载的最新模板或文档"""
def filedata_time_level01(path,title_len,name_title):
    try:
        list=[]
        for root,dirs,files in os.walk(path):
            for file in files:
                if file.__len__()==title_len:
                    if file[0:11]==name_title:
                        list.append(file)
                    else:
                        continue
            print(list.__len__())
            print(list)
            return list[list.__len__()-1]
    except IndexError as e:
        return False
        print(e)
# filedata_time_level01(name_title="长途区号2018",title_len=29,path=r"C:\Users\renqiwei\Downloads")

"""
所用用例位置：优化了基础数据识别问题
函数名：filedata_time_level01
        1.获取某模块下载的excel文档
        2.识别过滤其他模块文档
        3.自动识别最新的下载文档
"""
# def filedata_time_level01(path,title_len,name_title):
#     list=[]
#     # print(title_len, name_title)
#     for root,dirs,files in os.walk(path):
#         for file in files:
#
#             if file.__len__()==title_len:
#                 if file[0:11]==name_title:
#                     # print(file)
#                     list.append(file)
#                     # print(list)
#                 else:
#                     pass
#         # print(list.__len__())
#         # print(list)
#         return list[list.__len__()-1]
# # filedata_time_level01(name_title="长途区号2018",title_len=29,path=r"C:\Users\renqiwei\Downloads")

"""
callexe
#传参调用exe程序（解决相对路径，绝对路径问题），等待exe进程结束，此程序才结束。
# 调用方式　callexe(exe_file="import_Allzero.exe", exe_path=r"C:Usersrenqiwei\Desktop\study\exefile")
#需要用的模块：pywin32-214.win32-py2.5.exe
# 把该程序做成exe程序，就可以任何地方调用了（windows系统下）。
"""
# exe_path = sys.argv[1]
# exe_file = sys.argv[2]
def callexe(exe_path,exe_file):
    # exe_path =r"C:\Users\renqiwei\Desktop\study\exefile"
    # exe_file ="import.exe"
    os.chdir(exe_path)
    try:
        handle = win32process.CreateProcess(
            os.path.join(exe_path, exe_file),
            '',
            None,
            None,
            0,
            win32process.CREATE_NO_WINDOW,
            None ,
            exe_path,
            win32process.STARTUPINFO()
        )
        running = True
    except Exception :
        print ("Create Error!")
        handle = None
        running = False

    while running :
        rc = win32event.WaitForSingleObject(handle[0], 1000)
        if rc == win32event.WAIT_OBJECT_0:
                running = False
    #end while
    # print ("GoodBye")

def readExcel(self,path_file):
    workbook = xlrd.open_workbook(path_file)
    worksheets = workbook.sheet_names()                 #抓取所有sheet页的名称
    print('worksheets is %s' %worksheets)
    worksheet1 = workbook.sheet_by_name(u'灰名单号码')   #定位到sheet1
    """
    #通过索引顺序获取
    worksheet1 = workbook.sheets()[0]
    #或
    worksheet1 = workbook.sheet_by_index(0)
    """
    for worksheet_name in worksheets:           #遍历所有sheet对象
        worksheet = workbook.sheet_by_name(worksheet_name)
    print(worksheet)
    num_rows = worksheet1.nrows                 #遍历sheet1中所有行row
    for curr_row in range(num_rows):
        if curr_row >0:
            row = worksheet1.row_values(curr_row)
            print('%s %s' %(curr_row,row))
            return row
"""
函数名filedata_time_level01的低配版，识别某路径的下载文档
"""
def filedata(self,num):
    c=r"C:\Users\renqiwei\Downloads"
    self.num =0
    list=[]
    for root,dirs,files in os.walk(c):
        for file in files:
            os.path.join(root,file).encode('utf-8');
            if file.__len__()<23:
                pass
            else:
                list.append(file)
            num+=1
    return  file

"""
filedata_time_new的低级版本
"""
def filedata_list(self,num):
    c=r"C:\Users\renqiwei\Downloads"
    self.num =0
    list=[]
    for root,dirs,files in os.walk(c):
        for file in files:
            os.path.join(root,file).encode('utf-8');
            if file.__len__() < 20:
                pass
            else:
                list.append(file)
            num+=1
    return  list


"""
当不是该文档时，因文档名长度不一致，在提取文档名时提取失败 时长发生，
该函数方法繁冗识别率低
该函数在处置任务中使用，待下一版本剔除
"""
def filedata_time_new(self,num,c=r"C:\Users\renqiwei\Downloads"):
    self.num =0
    file_max=""
    for root,dirs,files in os.walk(c):
        for file in files:
            file_old=file
            year=file_old[5:9]
            month=file_old[10:12]
            day=file_old[13:15]
            hour =file_old[16:18]
            minute = file_old[19:21]
            s =file_old[22:24]
            print(year+month+day+hour+minute+s)
            file_old_spilt= year+month+day+hour+minute+s

            os.path.join(root,file).encode('utf-8');
            print(file[7:-5])
            file_new =file
            year=file_new[5:9]
            month=file_new[10:12]
            day=file_new[13:15]
            hour =file_new[16:18]
            minute = file_new[19:21]
            s =file_new[22:24]
            print(year+month+day+hour+minute+s)
            file_new_spilt= year+month+day+hour+minute+s
            print(type(file_new_spilt),type(file_old_spilt))

            if len(file_new_spilt)==14 and len(file_old_spilt)==14: #过滤长度,
               # 尝试try int(file_new_spilt) == int(file_old_spilt)   #筛选可以转换为int类型的数据
                assert len(file_new_spilt)== len(file_old_spilt)
                if file_new_spilt>=file_old_spilt:
                    file_max = file_new
                else:
                    file_old =file_max
                num+=1
            else:
                continue
            file1=file_max
            print(file1)
        return file1

"""
获得该路径下的文档个数，匹配下载数量是否是一个，目前因为本地与系统时间无法匹配，暂时无法匹配文档名
"""
def nu(self,num,path):
    self.num =0
    for root,dirs,files in os.walk(path):
        for file in files:
            os.path.join(root,file).encode('utf-8');
            num+=1
            fact_num = num
    return fact_num
