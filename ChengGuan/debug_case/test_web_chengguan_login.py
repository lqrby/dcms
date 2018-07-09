# -*- coding: utf-8 -*-
from PIL import Image
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from com.aliyun.api.gateway.sdk import client
# from com.aliyun.api.gateway.sdk.http import request
# from com.aliyun.api.gateway.sdk.common import constant
import base64
import json
import requests
import urllib.request
import os.path
import urllib
import time
import sys,http
from PIL import Image
from selenium import webdriver
import time
from PIL import ImageGrab
import traceback
from bs4 import BeautifulSoup
from test_web_chengguan_authCode import test_login_authCode
from test_getCookie import test_getCookie
from constant.constants import IP
#import test_case.HuJiaoXiTong import test_hujiao_main
#from test_case.HuJiaoXiTong
#@unittest.skip('暂时跳过该用例的测试')
class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            print("start test")  
            pass  
    def tearDown(self):             #与setUp()相对y  
            print("end test")  
            pass  
'''接口名称：web_城管系统_登录'''             
class test_web_chengguan_login(unittest.TestCase):   #把这个接口封装一个类，下面的方法是具体的测试用例  
    def test_chengguan_login(self):  #登录的方法
        #driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        driver.find_element_by_name('logonname').click()
        driver.find_element_by_name('logonname').send_keys(u"all")
        driver.find_element_by_name('logonpassword').click()
        driver.find_element_by_name('logonpassword').send_keys(u"all")
        driver.find_element_by_name('code').click()
        driver.find_element_by_name('code').send_keys(authCode)
        driver.find_element_by_xpath('//*[@id="logonForm"]/p/input').click()
        print("登录成功")
        # cookiestr = test_getCookie()
        # print ("这是从方法中调用的cookie：",cookiestr)  

    def test_chengguan_success(self):
        # #cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]  
        # session = requests.session()
        # #session.post(url = self.url,data = self.data,headers = self.headers,timeout=60) 
        # cookie = requests.utils.dict_from_cookiejar(session.cookies)
        try:
            header = {'cookie':cookiestr} 
            url = IP+"/dcms/bmsAdmin/Admin-redirectLogonPage.action"
            wbdata = requests.get(url,headers=header).text
            soup = BeautifulSoup(wbdata,'html.parser')
            print ("返回结果：",soup)
            
        except:
            traceback.print_exc() 
if __name__=="__main__":
    driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
    authCode = test_login_authCode(driver)
    cookiestr = test_getCookie(driver)
    while authCode == "" :
        authCode = test_login_authCode(driver) 
    else:
        unittest.main()
   


    
