# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from chengguan_login import test_cg_login

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
   
    def setUp(self): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            self.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")#获取浏览器对象
            print("start test")  

    def test_hujiaoMain(self):
        test_cg_login(self.driver)    
        #unittest.main()

    def tearDown(self):             #与setUp()相对y  
            print("end test")  
    

if __name__=="__main__":
    unittest.main()