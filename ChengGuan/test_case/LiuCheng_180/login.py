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
    def __init__(self,driver,url,userData):
        self.url = url
        self.driver = driver
        self.userData = userData
    def test_web_login(self):  #登录的方法
        loginResult = False
        authCode = test_login_authCode(self.driver,self.url) #获取验证码
        while authCode == "" :
            authCode = test_login_authCode(self.driver,self.url) 
        else:
            self.driver.find_element_by_name('logonname').click()
            self.driver.find_element_by_name('logonname').send_keys(u"wangnannan")
            time.sleep(1)
            self.driver.find_element_by_name('logonpassword').click()
            self.driver.find_element_by_name('logonpassword').send_keys(u"zswdmm")
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

    #市民登录
    def test_app_sm_login(self):  
        # sm_data = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/sm_login.txt")
        # smdata = sm_data.split(",")
        loginName = self.userData['sm']['loginName']
        password = self.userData['sm']['password']
        smloginurl = getConstant.IP_WEB_91+"/publicworkstation/userManage/pwdLogin.action?loginName="+loginName+"&password="+password+"&systemversion=7.0&token=&appversion=16&phonemodel=HONOR%20BLN-AL30&operatesystem=Android&is_login="
        respons = requests.get(url = smloginurl).text
        smLoginResult = json.loads(respons)
        if 'message' in smLoginResult and smLoginResult['message'] == '查询成功':
            print("市民apk:登录成功")
            return smLoginResult
        else:
            print("市民apk:登录失败")
            return False
        
    #执法局登录 
    def test_app_zfj_login(self):
        # zfjdata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/zfj_login.txt")
        # zfjList = zfjdata.split(",")
        zfj_url = getConstant.IP_WEB_91+"/dcms/PwasAdmin/mobile-loginadmin.action"
        zfj_data = {
            "role":self.userData['zfj']['role'],
            "logonname":self.userData['zfj']['logonname'],
            "logonpassword":self.userData['zfj']['logonpassword']
        }  
        res = requests.post(zfj_url,zfj_data).text
        zfjResult = json.loads(res)
        if 'message' in zfjResult and zfjResult['message'] == 'success':
            print("执法局apk:登录成功")
            return zfjResult
        else:
            print("执法局apk:登录失败！！！")
            return False

    #权属单位登录 
    def test_app_qsdw_login(self):
        # qsdwdata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/qsdw_login.txt")
        # qsdwList = qsdwdata.split(",")
        qsdw_url = getConstant.IP_WEB_91+"/dcms/PwasAdmin/mobile-loginadmin.action"
        qsdw_data = {
            "role":self.userData['qsdw']['role'],
            "logonname":self.userData['qsdw']['logonname'],
            "logonpassword":self.userData['qsdw']['logonpassword']
        }  
        qsdw_res = requests.post(qsdw_url,qsdw_data).text
        qsdwResult = json.loads(qsdw_res)
        if 'message' in qsdwResult and qsdwResult['message']== 'success':
            print("权属单位apk:登录成功")
            return qsdwResult
        else:
            print("权属单位apk:登录失败！！！")
            return False


    #网格管理员登录 
    def test_app_wggly_login(self):
        # wgglydata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/wggly_login.txt")
        # wgglyList = wgglydata.split(",")
        wggly_url = getConstant.IP_WEB_91+"/dcms/PwasAdmin/mobile-loginadmin.action"
        wggly_data = {
            "role":self.userData['wggly']['role'],
            "logonname":self.userData['wggly']['logonname'],
            "logonpassword":self.userData['wggly']['logonpassword']
        }  
        wggly_res = requests.post(wggly_url,wggly_data).text
        wgglyResult = json.loads(wggly_res)
        if 'message' in wgglyResult and wgglyResult['message']== 'success':
            print("网格管理员apk:登录成功")
            return wgglyResult
        else:
            print("XXXXXXXXXX网格管理员apk:登录失败XXXXXXXXXX")
            return False

    def test_app_allLogin(self):
        sm = self.test_app_sm_login()
        zfj = self.test_app_zfj_login()
        qsdw = self.test_app_qsdw_login()
        wggly = self.test_app_wggly_login()
        if sm and zfj and qsdw and wggly:
            print("移动端:*apk登录成功")
            loginObj = {"sm":sm,"zfj":zfj,"qsdw":qsdw,"wggly":wggly}
            # path = "E:/test/dcms/ChengGuan/test_case/LiuCheng_91/common/appLoginResult.txt"
            path = "E:/test/dcms/ChengGuan/common/appLoginResult.txt"
            writeAndReadTextFile().test_write_txt(path,str(loginObj))
            

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
    
