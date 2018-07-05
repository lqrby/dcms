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
import os.path
import urllib
import time
import urllib, sys
from PIL import Image
from selenium import webdriver
import time
from PIL import ImageGrab
#     '''''接口名称：web_城管系统_获取验证码'''             
def login_authCode():  #def test_jcjs_cl_post(self): 工单录入的方法
        url='http://219.149.226.180:7897/dcms/bms/login.jsp'
        driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        driver.maximize_window()  #将浏览器最大化
        driver.get(url)
        driver.save_screenshot('./result/yzm.png')  #截取当前网页，该网页有我们需要的验证码
        imgelement = driver.find_element_by_id('codeimg')  #定位验证码
        location = imgelement.location  #获取验证码x,y轴坐标
        size=imgelement.size  #获取验证码的长宽
        print("验证码图片坐标是:",location)
        print("验证码的长宽:",size)
        #rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
        rangle = (1200,495,1280,525)
        #rangle = (800,325,882,405)
        #print("box的类型是：",type(box))
        print("元组是不是图片坐标",rangle)

        #写成我们需要截取的位置坐标
        i=Image.open("./result/yzm.png") #打开截图
        #i.show()
        frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4.save("./result/yzm2.png")
        #frame4.show()
        print('ok=============================================')
        host = 'http://vercode.market.alicloudapi.com'
        path = '/vercode/info'
        method = 'POST'
        appcode = 'a887277961434056917f2e5190c55792'
        querys = ''
        bodys = {}
        url = host + path
        uploadfilepath = "./result/yzm2.png"
        f = open(uploadfilepath,'rb')
        fdata = base64.b64encode(f.read())
        print("fdata:",fdata)
        f.close()
        bodys['codeType'] = '''8003'''
        bodys['imageBase64'] = fdata
        post_data = urllib.parse.urlencode(bodys).encode(encoding='UTF8')
        req = urllib.request.Request(url, post_data)
        req.add_header('Authorization', 'APPCODE ' + appcode)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        response = urllib.request.urlopen(req)
        r = response.read()
        data = json.loads(r)
        print(data)
        result=data.get("result")
        print(result)
        return result

if __name__=='__main__':
    login_authCode()


