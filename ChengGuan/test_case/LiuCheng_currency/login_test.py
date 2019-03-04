# -*- coding: utf-8 -*-
import json
import requests
import sys
import time
# from config.Log import logging
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append("E:/test/dcms/ChengGuan")
from common.writeAndReadText import writeAndReadTextFile
from chengguan_authCode import test_login_authCode
from common.constant_all import getConstant

class allLogin():
    def __init__(self,driver,url):
        self.url = 'http://219.149.226.180:7897/dcms/bms/login.jsp'
        self.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        
    def test_web_login(self):  #登录的方法
        authCode = test_login_authCode(self.driver,self.url) #获取验证码
        while authCode == "" :
            authCode = test_login_authCode(self.driver,self.url) 
        else:
            self.driver.find_element_by_name('logonname').click()
            self.driver.find_element_by_name('logonname').send_keys('wangnannan')
            time.sleep(1)
            self.driver.find_element_by_name('logonpassword').click()
            self.driver.find_element_by_name('logonpassword').send_keys('123456')
            time.sleep(1)
            self.driver.find_element_by_name('code').click()
            self.driver.find_element_by_name('code').send_keys(authCode)
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="logonForm"]/p/input').click()
            if "智慧化城市管理云平台" in self.driver.page_source:
                loginResult = BeautifulSoup(self.driver.page_source,'html.parser')
                input = loginResult.find('input', attrs={'id': 'sysMenu'})
                #获取了input中的value属性值
                inputvalue = input['value']
                lginpath = 'E:/test/dcms/ChengGuan/common/webLoginResult.txt'
                writeAndReadTextFile().test_write_txt(lginpath,inputvalue)
                cookiestr = writeAndReadTextFile().test_getCookie(self.driver)
                print("cookies:",cookiestr)
                # 把cookie写入txt文件
                cook_path = "E:/test/dcms/ChengGuan/common/cookie.txt"
                writeAndReadTextFile().test_write_txt(cook_path,cookiestr)
                print("web登录成功")    
                return True
            else:
                print("web登录失败,用户名密码或验证码错误") 
                # return False
                self.test_web_login()

    

# if __name__=="__main__":
#     userData = {}
#     driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
#     url= getConstant.IP_WEB_91+'/dcms/bms/login.jsp'
#     userData = { 
#         'sm':{'loginName':'13161577834','password':'111111'},
#         'wggly':{'role':'2','logonname':'glyld','logonpassword':'111111'},
#         'qsdw':{'role':'6','logonname':'hbj','logonpassword':'111111'},
#         'zfj':{'role':'5','logonname':'zfj','logonpassword':'111111'},
        
#     }
#     login = allLogin(driver,url,userData)
#     login.test_web_login()
#     login.test_app_allLogin()
    
