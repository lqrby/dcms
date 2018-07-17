# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json  
import unittest
import urllib, sys, io
sys.path.append("E:/test/dcms/ChengGuan")
import time
# import config
from config.Log import logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from chengguan_login import test_cg_login
from common.getCookie import test_getCookie
from common.constant_all import getConstant



def test_goToWorkOrderEntry(driver):
    time.sleep(1)
    loginReturn = test_cg_login(driver)
    # print("登录返回值是：",loginReturn)
    cookiestr = test_getCookie(driver)
    print("呼叫系统获取到的cookie是：", cookiestr)
    imgObj = loginReturn.find('img', attrs={'id': 'hf'})

    while str(imgObj) == "":
        loginReturn = test_cg_login(driver)
        imgObj = loginReturn.find('img', attrs={'id': 'hf'})
    else:
        url = getConstant.IP+"/dcms/bmsAdmin/Admin-subsystem.action?systemId=402880ea2f6bd924012f6c521e8c0034"
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer":"http://219.149.226.180:7897/dcms/bmsAdmin/Admin-redirectLogonPage.action",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":cookiestr
            }
        r = requests.get(url,headers=header).text
        # print("结果是：============",r,"类型是：*****************",type(r))
        # res = json.loads(r.text)
        
        return r
       
       
def test_submitOrder(driver):
    res_result = test_goToWorkOrderEntry(driver) #进入呼叫页面的返回值
    
    cookies = test_getCookie(driver)
    submiturl = getConstant.IP+"/dcms/ccsCase/Case-callToCaseStart.action"
    file_handle = open('E:/test/dcms/ChengGuan/test_case/HuJiaoXiTong/test_data/gongdanluru.txt','r',encoding='utf8')
    print("....................................................")
    # print("进入呼叫系统的返回值是：", res_result)
    obj_data = file_handle.read()
    objdata = eval(obj_data)
    # print("objdata的类型是",type(objdata))
    # print("objdata的值是：",objdata)
    file_handle.close()
    header = {
        # "Content-Type":"multipart/form-data; boundary=----WebKitFormBoundaryBtxMo0J4B3oDgR89",
        # "Content-Type":"application/x-www-form-urlencoded",  
        # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding":"gzip, deflate",
        # "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
        "Cookie":cookies
    }
    # print("henders是：",header)
    #重定向没有返回值
    requests.post(url=submiturl,data=objdata,headers=header)
    print("工单提交成功")
    #重定向url
    list_url = getConstant.IP+"/dcms/ccsCase/Case-callsavelist.action?menuId=402880822f9490ad012f949eb313008a"
    respons = requests.get(list_url,headers=header).text
    # print("以下是结果：",respons)
      
if __name__=="__main__": 
        driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe") 
        # # test_goToWorkOrderEntry(driver)
        test_submitOrder(driver)
        # driver.close()