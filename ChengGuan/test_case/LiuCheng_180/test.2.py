# coding:utf-8
# -*- coding: utf-8 -*-
import re
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time,json
from config.Log import logging
from selenium import webdriver
from common.constant_all import getConstant
from login import allLogin
from jobEntry import submitOrder
from queRen import confirm
from heShi import verify
from liAn import setUpCase
from paiFa import distribution
from chuLi import fileFandling
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile


import threading,time
class thread_test(object):
    def __init__(self,sleep_time,name):
        self.sleep_time = sleep_time
        self.name=name
    def output(self):
        time.sleep(self.sleep_time)
        print(self.name)
a=thread_test(1,'a')
b=thread_test(4,'b')
c=thread_test(2,'c')
t_list=[]
for method in [a,b,c]:
    t = threading.Thread(target=method.output)
    t_list.append(t)
    t.start()
for t in t_list:#等待所有子线程都运行完，才往下走，可以尝试下把这个for循环注释掉，会发现打印顺序变成了end->a->c->b
    t.join()#join，等待子线程运行完成
print('end')