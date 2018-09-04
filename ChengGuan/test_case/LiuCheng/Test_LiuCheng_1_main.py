# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time,random
from config.Log import logging
from selenium import webdriver
from login import allLogin
from jobEntry import submitOrder
from queRen import confirm
from heShi import verify
from liAn import setUpCase
from paiFa import distribution
from chuLi import fileFandling
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        time.sleep(1)
        logging.info("打开浏览器")
    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("关闭浏览器")

    #web端登录
    def test_1webLogin(self):
        time.sleep(random.randint(1,2))
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        logging.info("*****1.web端登录完毕*****")

    # #移动端登录
    def test_2apkLogin(self):
        time.sleep(random.randint(1,3))
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        logging.info("*****2.移动端登录完毕*****")

    
    #web端工单录入
    def test_3gongDan(self):
        time.sleep(random.randint(8,15))
        webgdlr_res = submitOrder().test_web_submitOrder()
        if webgdlr_res:
            logging.info("*****3.web工单录入完毕*****")

    #web端立案
    def test_4liAn(self):
        time.sleep(random.randint(1,3)) 
        lian_result = setUpCase().test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")


    #web端派发
    def test_5paiFa(self):
        time.sleep(random.randint(1,5))  
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['qsdw']['user']
        item = {}
        item['id'] = loginItem_qsdw['id']
        item["deptname"] = loginItem_qsdw['deptname']
        item["dispatchDeptname"] = loginItem_qsdw['deptname']
        item["deptid"] = loginItem_qsdw['deptid']
        paifa_result = distribution().test_sendDetailsAndSendOut(item)
        if paifa_result:
            logging.info("*****5.web派发完毕*****")

    # 处理 移动端权属单位apk处理 
    def test_6chuLi(self):
        time.sleep(random.randint(1,5)) 
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['qsdw']['user']
        qsdw_result = fileFandling().test_app_handlingDetailsAndHandling(loginItem_qsdw)
        if qsdw_result:
            logging.info("*****6.移动端权属单位处理完毕*****")

    # 复核 网格管理员apk复核 
    def test_7fuHe(self):
        time.sleep(random.randint(1,5)) 
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        fh_loginUser = loginItemsUser['wggly']['user']
        wggly_result = reviewAndReturnVisit().test_app_returnDetailsAndVisit(fh_loginUser)
        if wggly_result:
            logging.info("*****7.移动端网格管理员复核完毕*****")

if __name__=="__main__":
    unittest.main()