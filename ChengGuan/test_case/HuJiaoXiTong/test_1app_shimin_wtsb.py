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



#提交工单录入表单    
def test_submitOrder():
    # test_goToWorkOrderEntry() #进入工单录入页面的返回值
    cookies = test_readCookies()
    submiturl = getConstant.IP+"/dcms/ccsCase/Case-callToCaseStart.action"
    file_handle = open('E:/test/dcms/ChengGuan/testFile/gongdanluru_2.txt','r',encoding='utf8')
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