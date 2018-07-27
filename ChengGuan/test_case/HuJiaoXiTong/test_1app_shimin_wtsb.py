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



#市民问题上报  
def test_submitOrder():
    # cookies = test_readCookies()
    submiturl = getConstant.IP+"/dcms/ccsCase/Case-callToCaseStart.action"
    file_handle = open('E:/test/dcms/ChengGuan/testFile/gongdanluru_2.txt','r',encoding='utf8')
    obj_data = file_handle.read()
    objdata = eval(obj_data)
    file_handle.close()
    # header = {
    #     "Cookie":cookies
    # }
    #重定向没有返回值
    requests.post(url=submiturl,data=objdata)
    print("工单提交成功")
    #重定向url
    list_url = getConstant.IP+"/dcms/cwsCase/Case-startlist.action?menuId=4028338158a414bd0158a4848a7f000d&keywords=402880ea2f6bd924012f6c521e8c0034"
    respons = requests.get(list_url).text
    return respons
if __name__=="__main__": 
        test_submitOrder()
        # driver.close()