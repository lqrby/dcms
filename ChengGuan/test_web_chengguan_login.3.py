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
from test_web_chengguan_authCode import login_authCode

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            print("start test")  
            pass  
    def tearDown(self):             #与setUp()相对y  
            print("end test")  
            pass  
'''''接口名称：web_城管系统_登录'''             
class test_web_chengguan_login(MyTest):   #把这个接口封装一个类，下面的方法是具体的测试用例  

    def test_chengguan_login(self):  #登录的方法
        self.url = 'http://219.149.226.180:7897/dcms/bmsAdmin/Admin-logon.action'
        self.headers = {"Content-Type":"application/x-www-form-urlencoded"} 
        self.data = { #请求参数  
        'logonname':	'wangnannan',
        'ogonpassword':	'123',
        'code': authCode          
        }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。
        #requests.post(url = self.url,data = self.data,headers = self.headers,timeout=60)
        # request = requests.get(url = self.url,data = self.data,headers = self.headers, timeout=60)
        session = requests.session()
        result=session.post(url = self.url,data = self.data,headers = self.headers,timeout=60) 
        cookie = requests.utils.dict_from_cookiejar(session.cookies)
        print(cookie)

        #这是第二个登录请求
        self.url1 = "http://219.149.226.180:7897/dcms/bmsAdmin/Admin-redirectLogonPage.action"
        self.headers1 = {'Content-type': 'text/html;charset=utf-8'}
        # self.headers1 = {
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        #     'Cache-Control': 'no-cache',
        #     'Connection': 'keep-alive',
        #     'Cookie':'JSESSIONID ='%cookie%; __utmz=142352369.1530683884.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=142352369.168148995.1530683884.1530683884.1530686123.2',
        #     'Host': '219.149.226.180:7897',
        #     'Pragma': 'no-cache',
        #     'Referer': 'http://219.149.226.180:7897/dcms/bms/login.jsp',
        #     'Upgrade-Insecure-Requests': 1,
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        # } 
        
        result = requests.get(url = self.url1,headers = self.headers1,cookies=cookie, timeout=60)
       
        #session=requests.session()
        #具体要接口登录后才可以获得cookies

        print("第二个接口登录返回值：",result.text) 
    #     # cookie = requests.utils.dict_from_cookiejar(session.cookies)
       # print(cookie)
        
    
if __name__=="__main__":  
    authCode = login_authCode()
    while authCode == "" :
        authCode = login_authCode() 
    else:
        unittest.main()
   


    
