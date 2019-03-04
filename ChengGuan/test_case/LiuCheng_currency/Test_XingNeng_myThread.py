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
from Test_XN_globalVariable import RES_TIMES,GT5,LT5,LT3,MAXTIME,MINTIME,TOTAL,SUCC,FAIL,EXCEPT


# 创建一个 threading.Thread 的派生类  
class RequestThread(threading.Thread):  
    # 构造函数  
    def __init__(self, thread_name,loginUrl,loginData):  
        threading.Thread.__init__(self)  
        self.test_count = 0
        self.thread_name = thread_name
        self.loginUrl = loginUrl
        self.loginData = loginData
        
    # 线程运行的入口函数  
    def run(self):  
        self.test_performace() 
  
    def test_performace(self):  
        global TOTAL  
        global SUCC  
        global FAIL  
        global EXCEPT  
        global GT5  
        global LT5  
        global LT3  
        
        
        try:  
            login_result = self.userLogin() 
            # time_span = login_result.elapsed.total_seconds() #请求时长
            loginResult = json.loads(login_result.text)
            # res_times.append(time_span)
            if login_result.status_code == 200 and 'message' in loginResult and loginResult['message'] == 'success':
                TOTAL+=1  
                SUCC+=1  
            else:  
                TOTAL+=1  
                FAIL+=1  
            self.maxtime(time_span)  
            self.mintime(time_span)  
            if time_span>5:  
                GT5+=1  
            elif time_span<5:  
                LT5+=1     
                if time_span<3:
                    LT3+=1                   
        except Exception:  
            TOTAL+=1  
            EXCEPT+=1  
    def maxtime(self,ts):  
        global MAXTIME  
        # print(ts)  
        if ts>MAXTIME:  
            MAXTIME=ts  
    def mintime(self,ts):  
        global MINTIME  
        if ts<MINTIME:  
            MINTIME=ts  

    def userLogin(self):
        global time_span
        global RES_TIMES
        response = requests.post(self.loginUrl,self.loginData,timeout=1,allow_redirects=False)
        time_span = response.elapsed.total_seconds() #请求时长
        RES_TIMES.append(time_span)
        return response

    def fanhuizhi(self):
        return RES_TIMES,GT5,LT5,LT3,MAXTIME,MINTIME,TOTAL,SUCC,FAIL,EXCEPT


