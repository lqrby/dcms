# -*- coding: utf-8 -*-
import re
import unittest
import sys,random
sys.path.append("E:/test/dcms/ChengGuan")
import time,json,requests
from config.Log import logging
from selenium import webdriver
from common.constant_all import getConstant
from common.writeAndReadText import writeAndReadTextFile
import threading#, httplib 
import openpyxl 
from test_case.LiuCheng_currency.new_personnel_zx180 import readExcel
from Test_XingNeng_myThread import RequestThread

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    
    def test_main(self):
        
        print('===========task start===========')  
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7897
            filename = 'E:/test/dcms/ChengGuan/testFile/newPersonnel/zfj_user_180.xlsx'
        else:
            ip = getConstant.IP
            filename = 'E:/test/dcms/ChengGuan/testFile/newPersonnel/zfj_user_91.xlsx' 
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
        # 并发的线程数  
        thread_count = ws.max_row-1
        loginUrl= ip+"/dcms/PwasAdmin/mobile-loginadmin.action"
        t_list=[]  #线程池
        for i in range(thread_count):  
            personData = readExcel(filename).readData(i+2)
            loginData = {
                "role":personData['jobposition'],
                "logonname":personData['logonname'],
                "logonpassword":personData['password']
            }  
            t = RequestThread("thread" + str(i),loginUrl,loginData)  
            t_list.append(t)
            t.start()  
        
        for t in t_list:  #等待所有子线程都运行完，才往下走，可以尝试下把这个for循环注释掉，会发现打印顺序变成了end->a->c->b
            t.join()   #join，等待子线程运行完成
        RES_TIMES,GT5,LT5,LT3,MAXTIME,MINTIME,TOTAL,SUCC,FAIL,EXCEPT = t.fanhuizhi()
        avgtime=sum(RES_TIMES)/len(RES_TIMES) 
        print("请求总数:%d,响应成功数:%d,响应失败数:%d,响应异常数:%d"%(TOTAL,SUCC,FAIL,EXCEPT))  
        print('最大响应时间:',MAXTIME)  
        print('最小响应时间:',MINTIME)  
        print('平均响应时间:',avgtime)  
        print('大于 5 秒:%d,百分比:%0.2f'%(GT5,(float(GT5) / TOTAL)*100),"%")  
        print('小于 5 秒:%d,百分比:%0.2f'%(LT5,(float(LT5) / TOTAL)*100),"%") 
        print('小于 3 秒:%d,百分比:%0.2f'%(LT3,(float(LT3) / TOTAL)*100),"%")  
        print('===========task end===========')  

if __name__ == "__main__":
    unittest.main()