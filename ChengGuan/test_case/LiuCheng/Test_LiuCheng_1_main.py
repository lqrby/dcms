# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from config.Log import logging
from selenium import webdriver
from login import allLogin
from jobEntry import test_submitOrder
from liAn import test_detailsAndFiling
from paiFa import test_sendDetailsAndSendOut
from chuLi import fileFandling
from fuHeAndHuiFang import test_reviewAndReturnVisit


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

    time.sleep(1)
    def test_1webLogin(self):
        #web端登录
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        logging.info("*****1.web端登录运行完毕*****")

    time.sleep(2)
    def test_2apkLogin(self):
        # #移动端登录
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        logging.info("*****2.移动端登录运行完毕*****")

    
    #web端工单录入
    time.sleep(2)
    def test_3gongDan(self):
        
        webgdlr_res = test_submitOrder().test_web_submitOrder()
        if webgdlr_res:
            logging.info("*****3.web工单录入完毕*****")

    #web端立案
    time.sleep(2)   
    def test_4liAn(self):
        lian_result = test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")


    #web端派发
    time.sleep(2)   
    def test_5paiFa(self):
        paifa_result = test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****5.web派发完毕*****")

    # 处理 移动端权属单位apk处理 
    time.sleep(2)   
    def test_6chuLi(self):
        qsdw_result = fileFandling().test_app_qsdw_handlingDetailsAndHandling()
        if qsdw_result:
            logging.info("*****6.移动端权属单位处理完毕*****")

    # 复核 网格管理员apk复核 
    time.sleep(2)   
    def test_7fuHe(self):
        wggly_result = test_reviewAndReturnVisit().test_app_wggly_returnDetailsAndVisit()
        if wggly_result:
            logging.info("*****7.移动端网格管理员复核完毕*****")

# if __name__=="__main__":
#     unittest.main()