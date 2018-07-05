# -*- coding: UTF-8 -*-#encoding=UTF-8

import requests
import sys
import json
import traceback
from test_web_chengguan_authCode import login_authCode
# -*- coding: utf-8 -*-
from PIL import Image
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
import os.path
import urllib
from time  import sleep
import urllib, sys
from bs4 import BeautifulSoup



url='http://219.149.226.180:7897/dcms/bms/login.jsp'
driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
driver.maximize_window()  #将浏览器最大化
driver.get(url)
driver.save_screenshot('yzm.png')  #截取当前网页，该网页有我们需要的验证码
imgelement = driver.find_element_by_id('codeimg')  #定位验证码
location = imgelement.location  #获取验证码x,y轴坐标
size=imgelement.size  #获取验证码的长宽
print("验证码图片坐标是:",location)
print("验证码的长宽:",size)
#rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
#rangle = (1393, 733, 1573, 798)
rangle = (1200,495,1280,525)
#rangle = (800,325,882,405)
#print("box的类型是：",type(box))
print("元组是不是图片坐标",rangle)

#写成我们需要截取的位置坐标
i=Image.open("yzm.png") #打开截图
#i.show()
frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save("yzm2.png")
#frame4.show()
host = 'http://vercode.market.alicloudapi.com'
path = '/vercode/info'
method = 'POST'
appcode = 'a887277961434056917f2e5190c55792'
querys = ''
bodys = {}
url = host + path
uploadfilepath = "yzm2.png"
f = open(uploadfilepath,'rb')
fdata = base64.b64encode(f.read())
print("fdata:",fdata)
f.close()
bodys['codeType'] = '''8003'''
bodys['imageBase64'] = fdata
post_data = urllib.parse.urlencode(bodys).encode(encoding='UTF8')
request = urllib.request.Request(url, post_data)
request.add_header('Authorization', 'APPCODE ' + appcode)
request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
response = urllib.request.urlopen(request)
r = response.read()
data1 = json.loads(r)
print(data1)
resultcode=data1.get("result")
print (resultcode) 
driver.find_element_by_name('logonname').click()
driver.find_element_by_name('logonname').send_keys(u"all")
driver.find_element_by_name('logonpassword').click()
driver.find_element_by_name('logonpassword').send_keys(u"all")
driver.find_element_by_name('code').click()
driver.find_element_by_name('code').send_keys(resultcode)
driver.find_element_by_xpath('//*[@id="logonForm"]/p/input').click()

sleep(10)
# data={      
# 'logonname':    '81eefa8d433e67f356fb874341def51e',
# 'logonpassword':    '81eefa8d433e67f356fb874341def51e',
# 'code': resultcode  }
cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]  
#print cookie  
  
cookiestr = ';'.join(item for item in cookie)  
print (cookiestr)  
print (cookie)
try:
        header =headers = {'cookie':cookiestr} 
        url = "http://219.149.226.180:7897/dcms/bmsAdmin/Admin-redirectLogonPage.action"
        wbdata = requests.get(url,headers=header).text
        soup = BeautifulSoup(wbdata,'html.parser')
        print (soup)
except:
    traceback.print_exc()    