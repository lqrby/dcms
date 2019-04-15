# -*- coding: utf-8 -*-
import re
import unittest
import sys,random
sys.path.append("E:/test/dcms/ChengGuan/")
import time,json
from config.Log import logging
from selenium import webdriver
from common.constant_all import getConstant
from common.writeAndReadText import writeAndReadTextFile
from login.login import allLogin
from zongHeChaXun import colligateQuery

# from login import allLogin
# from LiuCheng_currency.login import allLogin



class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        # cls.driver = webdriver.ChromeOptions()
        # cls.driver = webdriver.PhantomJS(executable_path="D:/python/chromeDriverSever/phantomjs-2.1.1-windows/bin/phantomjs.exe")
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
        elif '91' in getConstant.IP:
            ip = getConstant.IP
            userData = { 
                'sm':{'loginName':'13161577834','password':'111111'},
                'wggly':{'role':'2','logonname':'glyld','logonpassword':'gly!123456'},
                'qsdw':{'role':'6','logonname':'hbjld','logonpassword':'hbj!123456'},
                'zfj':{'role':'5','logonname':'zfjld','logonpassword':'zfj!123456'},
                
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
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()
        

    def test_liucheng(self):
        webLogin = self.loginObj.test_web_login()
        apkLogin = self.loginObj.test_app_allLogin()
        if webLogin and apkLogin:
            loginItems = writeAndReadTextFile().test_read_appLoginResult()
            loginItems['markNum'] = [2,1]
            colligateQuery(loginItems).test_web_zongHeDetail() #综合查询列表》案卷详情   
        else:
            time.sleep(905)
            self.test_liucheng()




    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("***关闭浏览器***")

if __name__=="__main__":
    unittest.main()