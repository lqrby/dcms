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
from new_personnel_zx180 import readExcel
from Test_XingNeng import RequestThread

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # 初始化移动端登录人员集合对象
        # cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        # #获取cookies
        # cls.cookies = writeAndReadTextFile().test_readCookies()
        pass
    def test_zfj_main(self):
        
        
        
        # 创建一个 threading.Thread 的派生类  
        print('===========task start===========')  
        res_times=[]#用list存放所有的响应时间
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
            personData['line'] = i+2
            t = RequestThread("thread" + str(i),loginUrl,personData)  
            t_list.append(t)
            t.start()  
            print("ttttttttttttttttttttttt",t[TOTAL])
        for t in t_list:  #等待所有子线程都运行完，才往下走，可以尝试下把这个for循环注释掉，会发现打印顺序变成了end->a->c->b
            t.join()   #join，等待子线程运行完成
        
        # avgtime=sum(res_times)/len(res_times) 
        # print("请求总数:%d,响应成功数:%d,响应失败数:%d,响应异常数:%d"%(TOTAL,SUCC,FAIL,EXCEPT))  
        # print('最大响应时间:',MAXTIME)  
        # print('最小响应时间:',MINTIME)  
        # print('平均响应时间:',avgtime)  
        # print('大于 5 秒:%d,百分比:%0.2f'%(GT5,(float(t[GT5]) / TOTAL)*100),"%")  
        # print('小于 5 秒:%d,百分比:%0.2f'%(LT5,(float(t[LT5]) / TOTAL)*100),"%") 
        # print('小于 3 秒:%d,百分比:%0.2f'%(LT3,(float(t[LT3]) / TOTAL)*100),"%")  
        # print('===========task end===========')  

    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")
        

if __name__=="__main__":
    
        unittest.main()
    
    