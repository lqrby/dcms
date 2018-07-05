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
#print("rangle的类型是：",type(rangle))
rangle = (1200,495,1280,525)
#print("box的类型是：",type(box))
print("元组是不是图片坐标",rangle)

#写成我们需要截取的位置坐标
i=Image.open("yzm.png") #打开截图
#i.show()
frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save("yzm2.png")
#frame4.show()
print('ok=============================================')
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
req = urllib.request.Request(url, post_data)
req.add_header('Authorization', 'APPCODE ' + appcode)
req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
response = urllib.request.urlopen(req)
r = response.read()
data = json.loads(r)
print(data)
result=data.get("result")
if result != "":
    
#json_result = json.dumps(result)
    print(result)
    time.sleep(1)
    class MyTest(unittest.TestCase):    #封装测试环境的初始化和还原的类  
        def setUp(self):     #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
                print("start test")
                pass  
        def tearDown(self):     #与setUp()相对  
                print("end test")  
                pass 
    '''''接口名称：web_城管系统_工单录入事件'''             
    class test_web_chengguan_login(MyTest):   #把这个接口封装一个类，下面的方法是具体的测试用例  
        '''''测试用例1：工单录入'''
        def chengguan_login(self):  #def test_jcjs_cl_post(self): 工单录入的方法
            time.sleep(2)
            self.url = 'http://219.149.226.180:7897/dcms/bmsAdmin/Admin-logon.action'
            #self.headers = {"Content-Type":"application/x-www-form-urlencoded "} 
            self.headers = {'Content-type': 'application/json'} 
            self.data = { #请求参数  
            'logonname':	'6763dcacda39d904e1f75a21d65efcd7',
            'ogonpassword':	'325afd63d2d64072b90d7a114db59008',
            'code': result
                
            }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。
            requests.post(url = self.url,data = self.data,headers = self.headers,timeout=30)                                     
        print("第一个执行完了")
        def chengguan_success(self):
            self.url = "http://219.149.226.180:7897/dcms/bmsAdmin/Admin-redirectLogonPage.action"
            self.headers = {'Content-type': 'application/json'}
            self.data = {}
            self.r = requests.post(url = self.url,data = self.data,headers = self.headers,timeout=30)         
        
            a=self.r.text 
            b =json.loads(a)
            c=str(b['sysId'])
            print(c)
        print("第二个执行完了")   
    # elem = driver.find_element_by_name("logonname").click()
    # elem = driver.find_element_by_name("logonname").send_keys("all")
    # time.sleep(1)
    # elem = driver.find_element_by_name("logonpassword").click()
    # elem = driver.find_element_by_name("logonpassword").send_keys("all")
    # time.sleep(1)
    # elem = driver.find_element_by_name("logonpassword").click()
    # time.sleep(1)
    # elem = driver.find_element_by_name("code").click()
    # elem = driver.find_element_by_name("code").send_keys(result)
    # time.sleep(1)
    # elem = driver.find_element_by_xpath('//*[@id="logonForm"]/p/input').click()
    # time.sleep(1)
    # # alert = driver.switch_to_alert()
    # # alert.accept() 点击js弹窗
        print("登录成功") 
else:
    print("很遗憾，验证码识别失败")
    
# time.sleep(10)
# elem=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/a[7]/div[1]/img').click()
# print("点击成功") 
# all_handles = driver.window_handles           # 获取当前窗口句柄集合（列表类型）
# driver.switch_to.window(all_handles[-1])   # 跳转到第num个窗口,0开头
# time.sleep(10)
# wait = WebDriverWait(driver, 30, 0.2)
# # wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "middlePage-id")))
# wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_id("middlePage-id")))
# #-------------------------------------进入呼叫系统管理模块
# # locator = (By.name, 'p_name')
# # try:
# #     WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
# #     print driver.find_element_by_link_text('CSDN').get_attribute('href')
# # finally:
# #     driver.close()
# # wait = WebDriverWait(driver, 30, 0.2)
# # # wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "middlePage-id")))
# # wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_id("middlePage-id")))
# # # driver.switch_to.frame("middlePage-id")
# time.sleep(5)
# elem = driver.find_element_by_id("p_name").click()
# elem = driver.find_element_by_name("p_name").send_keys(u"自动角色一")
# elem = driver.find_element_by_id("p_phone").click()
# elem = driver.find_element_by_id("p_phone").send_keys("13021979651")
# b = Select(driver.find_element_by_id('p_sex'))#课程标签下拉框
# b.select_by_value("男")#免费
# time.sleep(5)
# js='$("#gridid").attr("value","1000")'
# driver.execute_script(js)

