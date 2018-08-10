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
from common.writeAndReadText import writeAndReadTextFile
from chengguan_authCode import test_login_authCode
from common.constant_all import getConstant

def test_cg_login(driver):  #登录的方法
    loginResult = False
    authCode = test_login_authCode(driver) #获取验证码
    while authCode == "" :
        authCode = test_login_authCode(driver) 
    else:
        driver.find_element_by_name('logonname').click()
        driver.find_element_by_name('logonname').send_keys(u"wangnannan")
        time.sleep(1)
        driver.find_element_by_name('logonpassword').click()
        driver.find_element_by_name('logonpassword').send_keys(u"123456")
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
            input = loginResult.find('input', attrs={'id': 'sysMenu'})
            #获取了input中的value属性值
            inputvalue = input['value']
            lginpath = 'E:/test/dcms/ChengGuan/common/webLoginResult.txt'
            writeAndReadTextFile().test_write_txt(lginpath,inputvalue)
            # json_value = json.loads(inputvalue)
            cookiestr = writeAndReadTextFile().test_getCookie(driver)
            print("cookies:",cookiestr)
            # 把cookie写入txt文件
            cook_path = "E:/test/dcms/ChengGuan/common/cookie.txt"
            writeAndReadTextFile().test_write_txt(cook_path,cookiestr)

    return loginResult


if __name__=="__main__":
     driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
     test_cg_login(driver)


    
