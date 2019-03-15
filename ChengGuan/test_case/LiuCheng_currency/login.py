# -*- coding: utf-8 -*-
import json
import requests
import sys,random
import time
# from config.Log import logging
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append("E:/test/dcms/ChengGuan")
from common.writeAndReadText import writeAndReadTextFile
from chengguan_authCode import test_login_authCode
from common.constant_all import getConstant

class allLogin():
    def __init__(self,driver,url,userData):
        self.url = url
        self.driver = driver
        self.userData = userData
        self.header = {
            "User-Agent": "Android/8.0.0",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }
    def test_web_login(self):  #登录的方法
        if '180' in self.url:
            name = 'zx'
            password = 'zx!123456'
        elif '15' in self.url:
            name = 'gaoquan'
            password = 'gq!123456'
        else:
            name = 'syl'
            password = 'syl!123456'
        authCode,image_split_arr = test_login_authCode(self.driver,self.url) #获取验证码
        while authCode == "" :
            time.sleep(random.randint(1,2))
            authCode = test_login_authCode(self.driver,self.url) 
        else:
            self.driver.find_element_by_name('logonname').click()
            self.driver.find_element_by_name('logonname').send_keys(name)
            time.sleep(1)
            self.driver.find_element_by_name('logonpassword').click()
            self.driver.find_element_by_name('logonpassword').send_keys(password)
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
                print("XXXXXXXXXXXXXweb登录失败,用户名密码或验证码错误XXXXXXXXXXXXXXX")
                for i,imgItem in enumerate(image_split_arr):
                    outDir = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
                    imgItem.save("E:/test/dcms/ChengGuan/common/image/"+ outDir + str(i) + ".png")
                time.sleep(random.randint(1,3))
                self.test_web_login()

    # 市民登录
    def test_app_sm_login(self):  
        loginName = self.userData['sm']['loginName']
        password = self.userData['sm']['password']
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7880
        else:
            ip = getConstant.IP
        sm_header = {
            "Cache-Control":"no-cache/no-store",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "User-Agent":"okhttp/3.2.0"
        }
        smloginurl = ip+"/publicworkstation/userManage/pwdLogin.action?loginName="+loginName+"&password="+password+"&systemversion=7.0&token=&appversion=16&phonemodel=HONOR%20BLN-AL30&operatesystem=Android&is_login="
        sm_respons = requests.get(url = smloginurl,headers = sm_header,timeout = 20)
        sm_respons.connection.close()
        if '查询成功' in sm_respons.text:
            print("市民apk:登录成功")
            return json.loads(sm_respons.text)
        else:
            print("XXXXXXXXXXXXXXXXXX市民apk:登录失败XXXXXXXXXXXXXXXXXXX")
            return False
        
    #执法局登录 
    def test_app_zfj_login(self):
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7897
        else:
            ip = getConstant.IP
        zfj_url = ip+"/dcms/PwasAdmin/mobile-loginadmin.action"
        
        zfj_data = {
            "role":self.userData['zfj']['role'],
            "logonname":self.userData['zfj']['logonname'],
            "logonpassword":self.userData['zfj']['logonpassword']
        }  
        zfj_res = requests.post(zfj_url,zfj_data,headers = self.header,timeout = 20)
        zfj_res.connection.close()
        if 'success' in zfj_res.text:
            print("执法局apk:登录成功")
            return json.loads(zfj_res.text)
        else:
            print("XXXXXXXXXXXXXXXXXXXXX执法局apk:登录失败XXXXXXXXXXXXXXXXXXX")
            return False

    #权属单位登录 
    def test_app_qsdw_login(self):
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7897
        else:
            ip = getConstant.IP
        qsdw_url = ip+"/dcms/PwasAdmin/mobile-loginadmin.action"
        qsdw_data = {
            "role":self.userData['qsdw']['role'],
            "logonname":self.userData['qsdw']['logonname'],
            "logonpassword":self.userData['qsdw']['logonpassword']
        }  
        qsdw_res = requests.post(qsdw_url,qsdw_data,headers = self.header,timeout = 20)
        qsdw_res.connection.close()
        if 'success' in qsdw_res.text:
            print("权属单位apk:登录成功")
            return json.loads(qsdw_res.text)
        else:
            print("XXXXXXXXXXXXXXXX权属单位apk:登录失败XXXXXXXXXXXXXXX")
            return False


    #网格管理员登录 
    def test_app_wggly_login(self):
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7897
        else:
            ip = getConstant.IP
        wggly_url = ip+"/dcms/PwasAdmin/mobile-loginadmin.action"
        wggly_data = {
            "role":self.userData['wggly']['role'],
            "logonname":self.userData['wggly']['logonname'],
            "logonpassword":self.userData['wggly']['logonpassword']
        }  
        wggly_res = requests.post(wggly_url,wggly_data,headers = self.header,timeout = 20)
        wggly_res.connection.close()
        if 'success' in wggly_res.text:
            print("网格管理员apk:登录成功")
            return json.loads(wggly_res.text)
        else:
            print("XXXXXXXXXXXXXXXX网格管理员apk:登录失败XXXXXXXXXXXXXXX")
            return False

    def test_app_allLogin(self):
        sm = self.test_app_sm_login()
        # sm = 'sm'
        zfj = self.test_app_zfj_login()
        qsdw = self.test_app_qsdw_login()
        wggly = self.test_app_wggly_login()
        if sm and zfj and qsdw and wggly:
            loginObj = {"sm":sm,"zfj":zfj,"qsdw":qsdw,"wggly":wggly}
            path = "E:/test/dcms/ChengGuan/common/appLoginResult.txt"
            writeAndReadTextFile().test_write_txt(path,str(loginObj))
            print("移动端:*apk登录成功")
            return True
            

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
    
