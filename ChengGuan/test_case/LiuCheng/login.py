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
    # def __init__(self,driver,):
    #     pass
    def test_web_login(self,driver):  #登录的方法
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
            if "智慧化城市管理云平台" in driver.page_source:
                loginResult = BeautifulSoup(driver.page_source,'html.parser')
                input = loginResult.find('input', attrs={'id': 'sysMenu'})
                #获取了input中的value属性值
                inputvalue = input['value']
                lginpath = 'E:/test/dcms/ChengGuan/common/webLoginResult.txt'
                writeAndReadTextFile().test_write_txt(lginpath,inputvalue)
                cookiestr = writeAndReadTextFile().test_getCookie(driver)
                print("cookies:",cookiestr)
                # 把cookie写入txt文件
                cook_path = "E:/test/dcms/ChengGuan/common/cookie.txt"
                writeAndReadTextFile().test_write_txt(cook_path,cookiestr)
                print("web登录成功")    
                loginResult = True
            else:
                print("web登录失败") 
                loginResult = False 
        return loginResult

            # try:
            #     assert u"智慧化城市管理云平台" in driver.page_source, u"页面源码中不存在该关键字！"
            # except AssertionError:
            #     print("断言验证错误")
            #     loginResult = self.test_web_login(driver)
            # else:
            #     print("登录后断言匹配正确")
            #     loginResult = BeautifulSoup(driver.page_source,'html.parser')
            #     input = loginResult.find('input', attrs={'id': 'sysMenu'})
            #     #获取了input中的value属性值
            #     inputvalue = input['value']
            #     lginpath = 'E:/test/dcms/ChengGuan/common/webLoginResult.txt'
            #     writeAndReadTextFile().test_write_txt(lginpath,inputvalue)
            #     # json_value = json.loads(inputvalue)
            #     cookiestr = writeAndReadTextFile().test_getCookie(driver)
            #     print("cookies:",cookiestr)
            #     # 把cookie写入txt文件
            #     cook_path = "E:/test/dcms/ChengGuan/common/cookie.txt"
            #     writeAndReadTextFile().test_write_txt(cook_path,cookiestr)
            #     # print(loginResult)
            #     return loginResult

    #市民登录
    def test_app_sm_login(self):  
        sm_data = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/sm_login.txt")
        smdata = sm_data.split(",")
        loginName = smdata[0]
        password = smdata[1]
        smloginurl = getConstant.IP_APP_180+"/publicworkstation/userManage/pwdLogin.action?loginName="+loginName+"&password="+password+"&systemversion=7.0&token=&appversion=16&phonemodel=HONOR%20BLN-AL30&operatesystem=Android&is_login="
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
        zfjdata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/zfj_login.txt")
        zfjList = zfjdata.split(",")
        zfj_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/mobile-loginadmin.action"
        zfj_data = {
            "role":zfjList[0],
            "logonname":zfjList[1],
            "logonpassword":zfjList[2]
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
        qsdwdata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/qsdw_login.txt")
        qsdwList = qsdwdata.split(",")
        qsdw_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/mobile-loginadmin.action"
        qsdw_data = {
            "role":qsdwList[0],
            "logonname":qsdwList[1],
            "logonpassword":qsdwList[2]
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
        wgglydata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/login/wggly_login.txt")
        wgglyList = wgglydata.split(",")
        wggly_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/mobile-loginadmin.action"
        wggly_data = {
            "role":wgglyList[0],
            "logonname":wgglyList[1],
            "logonpassword":wgglyList[2]
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
            path = "E:/test/dcms/ChengGuan/common/appLoginResult.txt"
            writeAndReadTextFile().test_write_txt(path,str(loginObj))
            

if __name__=="__main__":
    driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
    allLogin().test_web_login(driver)
    # allLogin().test_app_allLogin()

    
