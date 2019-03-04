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

# main 代码开始  
# HOST = read_user() # #主机地址 例如192.168.1.101  
# PORT = 80 #端口  
# URI = "/?123" #相对地址,加参数防止缓存，否则可能会返回304  
TOTAL = 0 #总数  
SUCC = 0 #响应成功数  
FAIL = 0 #响应失败数  
EXCEPT = 0 #响应异常数  
MAXTIME = 0 #最大响应时间  
MINTIME = 100 #最小响应时间，初始值为100秒  
GT5 = 0 #统计大于5秒内响应的  
LT5 = 0 #统计小于5秒响应的  
LT3 = 0 #统计小于3秒响应的  
RES_TIMES = []
