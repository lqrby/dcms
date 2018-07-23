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
from test_2web_chengguan_login import test_cg_login
from common.getCookie import test_readCookies
from common.constant_all import getConstant


# 进入工单录入页面
# def test_goToWorkOrderEntry():
#     # time.sleep(1)
#     # loginReturn = test_cg_login(driver)
#     # print("登录返回值是：",loginReturn)
#     cookiestr = test_readCookies()
#     print("多少：",cookiestr)
#     # print("呼叫系统获取到的cookie是：", cookiestr)
#     # imgObj = loginReturn.find('img', attrs={'id': 'hf'})

#     # while str(imgObj) == "":
#     #     loginReturn = test_cg_login(driver)
#     #     imgObj = loginReturn.find('img', attrs={'id': 'hf'})
#     # else: 
#     url = getConstant.IP+"/dcms//ccsCase/Case-callinput.action?menuId=402880822f9490ad012f949e55720083&keywords=402880ea2f6bd924012f6c521e8c0034"
#     print("url:",url)
#     header = {
#         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
#         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Referer":"http://219.149.226.180:7897/dcms/bmsAdmin/Admin-redirectLogonPage.action",
#         "Accept-Encoding":"gzip, deflate",
#         "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
#         "Cookie":cookiestr
#         }
#     r = requests.get(url,headers=header).text
#     print("结果是：============",r,"类型是：*****************",type(r))
#     # res = json.loads(r.text)
    
#     return r
       
#提交工单录入表单gongdanluru_2.txt_无需核实复核   
def test_submitOrder():
    # test_goToWorkOrderEntry() #进入工单录入页面的返回值
    cookies = test_readCookies()
    submiturl = getConstant.IP+"/dcms/ccsCase/Case-callToCaseStart.action"
    file_handle = open('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_2.txt','r',encoding='utf8')
    obj_data = file_handle.read()
    objdata = eval(obj_data)
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
    #重定向没有返回值
    requests.post(url=submiturl,data=objdata,headers=header)
    print("工单提交成功")
    #重定向url
    list_url = getConstant.IP+"/dcms/cwsCase/Case-startlist.action?menuId=4028338158a414bd0158a4848a7f000d&keywords=402880ea2f6bd924012f6c521e8c0034"
    respons = requests.get(list_url,headers=header).text
    return respons
if __name__=="__main__": 
        test_submitOrder()
        # driver.close()