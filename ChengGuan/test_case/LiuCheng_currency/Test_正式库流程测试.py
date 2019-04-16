# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time,random,json
import threading
from config.Log import logging
from selenium import webdriver
# from login import allLogin
# from jobEntry import submitOrder
# from queRen import confirm
# from heShi import verify
# from liAn import setUpCase
# from paiFa import distribution
# from guaZhang import hangUp
# from chuLi import fileFandling
# from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from laiYuanTongJi import SourceStatistics
from zongHeChaXun import colligateQuery

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()
    
    
    #来源统计
    def laiYuanTongJi(self):
        time.sleep(random.randint(1,3))
        loginUser = {}
        SourceStatistics(loginUser).test_web_laiYuanTongJiList()
        SourceStatistics(loginUser).test_searchOrExport()

    

    def test_liucheng(self):
        # 来源统计
        self.laiYuanTongJi()

        # 综合查询
        loginItems = writeAndReadTextFile().test_read_appLoginResult()
        loginItems['markNum'] = [2,1]
        colligateQuery(loginItems).test_web_zongHeDetail() #综合查询列表》案件详情
        colligateQuery(loginItems).test_ExportThisPage()   #导出

        

if __name__=="__main__":
    
    unittest.main()
    
    