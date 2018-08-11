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
from test_liuCheng_all import liuCheng


class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
   
    # def setUp(self): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
    #     # print("start test")
    #     print("初始化")
        
    
    # def tearDown(self): 
    #     # self.driver.quit()            #与setUp()相对y  
    #     print("***end test***")  

    def test_apkLogin(self):
        print("方法一")
        # #移动端登录
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        print("************************************")
        # liuCheng().test_liucheng_1()
        #unittest.main()

    def test_webLogin(self):
        self.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        print("方法二")
        #web端登录
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        # self.driver.get('https://www.baidu.com/')
    

if __name__=="__main__":
    unittest.main()