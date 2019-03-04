# -*- coding: utf-8 -*-
import re
import unittest
import sys,random
sys.path.append("E:/test/dcms/ChengGuan")
import time,json,requests
from config.Log import logging
from selenium import webdriver
from common.constant_all import getConstant
# from login import allLogin
# from jobEntry import submitOrder
# from queRen import confirm
# from heShi import verify
# from liAn import setUpCase
# from paiFa import distribution
# from piSi import Approval
# from chuLi import fileFandling
# from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile
import threading#, httplib  
HOST = "https://www.baidu.com" #主机地址 例如192.168.1.101  
# PORT = 80 #端口  
# URI = "/?123" #相对地址,加参数防止缓存，否则可能会返回304  
TOTAL = 0 #总数  
SUCC = 0 #响应成功数  
FAIL = 0 #响应失败数  
EXCEPT = 0 #响应异常数  
MAXTIME=0 #最大响应时间  
MINTIME=100 #最小响应时间，初始值为100秒  
GT5=0 #统计大于5秒内响应的  
# LT8=0 #统计小于8秒响应的  
LT5=0 #统计小于5秒响应的  
LT3=0 #统计小于3秒响应的  
# 创建一个 threading.Thread 的派生类  
class RequestThread(threading.Thread):  
    # 构造函数  
    def __init__(self, thread_name,res_times):  
        threading.Thread.__init__(self)  
        self.test_count = 0  
  
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
        global res_times  
        
        try:  
            start_time = time.time()  #开始时间
            res = requests.get(HOST)  
            end_time = time.time() #结束时间
            time_span =  end_time - start_time  #请求时长
            print('%s:%f\n'%(self.name,time_span))
            res_times.append(time_span)
            if res.status_code == 200:  
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

if __name__ == "__main__":
    # main 代码开始  
    print('===========task start===========')  
    res_times=[]#用list存放所有的响应时间
    # 开始的时间  
    start_time = time.time()  
    # 并发的线程数  
    thread_count = 10
    t_list=[]  #线程池
    for i in range(thread_count):  
        t = RequestThread("thread" + str(i+1),res_times)  
        t_list.append(t)
        t.start()  
    
    for t in t_list:  #等待所有子线程都运行完，才往下走，可以尝试下把这个for循环注释掉，会发现打印顺序变成了end->a->c->b
        t.join()   #join，等待子线程运行完成
    
    avgtime=sum(res_times)/len(res_times) 
    print("请求总数:%d,响应成功数:%d,响应失败数:%d,响应异常数:%d"%(TOTAL,SUCC,FAIL,EXCEPT))  
    print('最大响应时间:',MAXTIME)  
    print('最小响应时间:',MINTIME)  
    print('平均响应时间:',avgtime)  
    print('大于 5 秒:%d,百分比:%0.2f'%(GT5,(float(GT5) / TOTAL)*100),"%")  
    print('小于 5 秒:%d,百分比:%0.2f'%(LT5,(float(LT5) / TOTAL)*100),"%") 
    print('小于 3 秒:%d,百分比:%0.2f'%(LT3,(float(LT3) / TOTAL)*100),"%")  
    print('===========task end===========')  