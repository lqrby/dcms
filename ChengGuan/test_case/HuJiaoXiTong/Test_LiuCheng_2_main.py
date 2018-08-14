# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
import json
import re
import ast
import unittest
import urllib, sys, io
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
# import config
from config.Log import logging
import unittest
from selenium import webdriver
from test_login import allLogin
# from test_liuCheng_all import liuCheng
from test_jobEntry import test_submitOrder
from test_queRen import test_web_UnconfirmedDetail
from test_heShi import test_app_zfj_daiHeShiDetail
from test_liAn import test_detailsAndFiling
from test_paiFa import test_sendDetailsAndSendOut
from test_chuLi import fileFandling
from test_fuHeAndHuiFang import test_reviewAndReturnVisit


class MyTest2(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        logging.info("***打开浏览器***")
    

    #web端登录
    def test_1webLogin_lc2(self):
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        logging.info("*****1.web端登录运行完毕*****")

    #移动端登录
    time.sleep(2)
    def test_2apkLogin_lc2(self):
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        logging.info("*****2.移动端登录运行完毕*****")

    #移动端市民上报案卷
    time.sleep(2)
    def test_3gongDan_lc2(self):
        sm_res = test_submitOrder().test_app_sm_submitOrder()
        if sm_res:
            logging.info("*****3.市民上报案卷完毕*****")

    #web端确认案卷
    time.sleep(2)
    def test_4queRen_lc2(self):
        webqueren_res = test_web_UnconfirmedDetail()
        if webqueren_res:
            logging.info("*****4.web确认案卷完毕*****")

    #移动端执法局核实案卷
    time.sleep(2)
    def test_5heShi_lc2(self):
        zfjhs_res = test_app_zfj_daiHeShiDetail()
        if zfjhs_res:
            logging.info("*****5.执法局核实案卷完毕*****")


    #web端立案   
    time.sleep(2)
    def test_6liAn_lc2(self):
        lian_result = test_detailsAndFiling()
        if lian_result:
            logging.info("*****6.web立案完毕*****")


    #web端派发 
    time.sleep(2)  
    def test_7paiFa_lc2(self):
        paifa_result = test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****7.web派发完毕*****")

    # 处理 移动端权属单位apk处理
    time.sleep(2)    
    def test_8chuLi_lc2(self):
        qsdw_result = fileFandling().test_app_qsdw_handlingDetailsAndHandling()
        if qsdw_result:
            logging.info("*****8.移动端权属单位处理完毕*****")

    # 复核 执法局复核
    time.sleep(2)    
    def test_9fuHe_lc2(self):
        zfjfh_result = test_reviewAndReturnVisit().test_app_zfj_returnDetailsAndVisit()
        if zfjfh_result:
            logging.info("*****9.移动端执法局复核完毕*****")

    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("***关闭浏览器***")

# if __name__=="__main__":
#     unittest.main()