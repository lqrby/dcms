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
import sys,http
from PIL import Image
import time
from PIL import ImageGrab
import traceback
from bs4 import BeautifulSoup
sys.path.append("E:/test/dcms/ChengGuan")
from common.getCookie import test_getCookie
from chengguan_authCode import test_login_authCode


def test_cg_login(driver):  #登录的方法
    loginResult = False
    authCode = test_login_authCode(driver) #获取验证码
    while authCode == "" :
        authCode = test_login_authCode(driver) 
    else:
        time.sleep(1)
        driver.find_element_by_name('logonname').click()
        driver.find_element_by_name('logonname').send_keys(u"wangnannan")
        time.sleep(1)
        driver.find_element_by_name('logonpassword').click()
        driver.find_element_by_name('logonpassword').send_keys(u"123")
        time.sleep(1)
        driver.find_element_by_name('code').click()
        driver.find_element_by_name('code').send_keys(authCode)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="logonForm"]/p/input').click()
        
        try:
            assert u"智慧化城市管理云平台" in driver.page_source, u"页面源码中不存在该关键字！"
        except AssertionError:
            print("断言验证错误")
            loginResult = test_cg_login(driver)
        else:
            print("登录后断言匹配正确")
            loginResult = BeautifulSoup(driver.page_source,'html.parser')
            cookiestr = test_getCookie(driver)
            print("登录后的cookie是",cookiestr)
        # finally:
        #     print("断言验证错误，我依然被执行。")
        
       
    return loginResult
        
       

   

            
# if __name__=="__main__":
#     driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
#     test_chengguan_login(driver)
#     driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
#     authCode = test_login_authCode(driver)
#     cookiestr = test_getCookie(driver)
#     while authCode == "" :
#         authCode = test_login_authCode(driver) 
#     else:
#         unittest.main()
#         t=test_web_chengguan_login(MyTest)
#         t.test_chengguan_login()
   


    
