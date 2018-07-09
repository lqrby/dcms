# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from test_web_chengguan_authCode import test_login_authCode
from test_web_chengguan_login import test_web_chengguan_login
from common.test_getCookie import test_getCookie


class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    unittest.TestCase.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")#获取浏览器对象  
    unittest.TestCase.authCode = test_login_authCode(unittest.TestCase.driver) #获取登录验证码
    unittest.TestCase.cookiestr = test_getCookie(unittest.TestCase.driver) #获取cookie
    def setUp(self): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            
            print("start test")  
            pass  

    def test_hujiaoMain(self):
        #cookiestr = test_getCookie(driver)
        while self.authCode == "" :
            self.authCode = test_login_authCode(unittest.TestCase.driver) 
        else:
            #unittest.main()
            
            print("执行登陆的两个方法")
            test_web_chengguan_login(unittest.TestCase)
            print("执行登陆完毕")    


    def tearDown(self):             #与setUp()相对y  
            
            print("end test")  
            pass  
#class test_web_hujiao_main(MyTest):   #把这个接口封装一个类，下面的方法是具体的测试用例  
    

    if __name__=="__main__":
        unittest.main()