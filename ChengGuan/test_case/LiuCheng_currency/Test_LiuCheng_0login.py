# -*- coding: utf-8 -*-
import re
import unittest
import sys,random
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
from piSi import Approval
from chuLi import fileFandling
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile



class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        logging.info("***打开浏览器***")
        # 初始化登录数据及登录类对象
        userData = {}
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7897
            userData = { 
                'sm':{'loginName':'13161577834','password':'123456'},
                'wggly':{'role':'2','logonname':'csgly','logonpassword':'gly!123456'},
                'qsdw':{'role':'6','logonname':'cshbj','logonpassword':'hbj!123456'},
                'zfj':{'role':'5','logonname':'cszfj','logonpassword':'zfj!123456'},
            }
            
        else:
            ip = getConstant.IP
            userData = { 
                'sm':{'loginName':'13161577834','password':'111111'},
                'wggly':{'role':'2','logonname':'glyld','logonpassword':'gly!123456'},
                'qsdw':{'role':'6','logonname':'hbjld','logonpassword':'hbj!123456'},
                'zfj':{'role':'5','logonname':'zfjld','logonpassword':'zfj!123456'},
                
            }
        
        url= ip+'/dcms/bms/login.jsp'
        print("url:",url)
        cls.loginObj = allLogin(cls.driver,url,userData)
        # 初始化移动端登录人员集合对象
        # cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        # #获取cookies
        # cls.cookies = writeAndReadTextFile().test_readCookies()
        
    #web端登录
    def test_1webLogin_lc5(self):
        webLogin = self.loginObj.test_web_login()
        while webLogin==False:
            webLogin = self.loginObj.test_web_login()
        logging.info("*****1.web端登录完毕*****")

    #移动端登录
    def test_2apkLogin_lc5(self):
        time.sleep(random.randint(1,3)) 
        appLogin = self.loginObj.test_app_allLogin()
        while appLogin == False:
            appLogin = self.loginObj.test_app_allLogin()
        logging.info("*****2.移动端登录完毕*****")

    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("***关闭浏览器***")

if __name__=="__main__":
    unittest.main()