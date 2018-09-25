# -*- coding: utf-8 -*-
from PIL import Image
import unittest
import base64
import json
import requests
import os
import urllib
import time
import sys
# os.chdir('E:/test/dcms/ChengGuan/common/identifyingCode')
from selenium import webdriver
# from config.Log import logging
from PIL import Image
import time
from PIL import ImageGrab
sys.path.append("E:/test/dcms/ChengGuan")
sys.path.append('E:/test/dcms/ChengGuan/common/identifyingCode')
from common.constant_all import getConstant
from common.identifyingCode.verification_code import verificationCode

# path1=os.path.abspath('.')   # 表示当前所处的文件夹的绝对路径
# print("地址是：",path1 )
#     '''''接口名称：web_城管系统_获取验证码'''
# driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")             
def test_login_authCode(driver,url):  #def test_jcjs_cl_post(self): 工单录入的方法
        # url= getConstant.IP_WEB_91+'/dcms/bms/login.jsp'
        driver.maximize_window()  #将浏览器最大化  1535, 863
        # driver.set_window_size(1024, 768)
        driver.implicitly_wait(30)#隐式等待
        driver.get(url)
        driver.save_screenshot('E:/test/dcms/ChengGuan/result/yzm.png')  # 截取当前页面全图
        element = driver.find_element_by_id("codeimg")  # 验证码标签对象
        location = element.location
        # print("获取元素坐标：",location)
        # 计算出元素上、下、左、右 位置
        left = element.location['x']
        top = element.location['y']+86
        right = left + element.size['width']
        bottom = top + element.size['height']
        im = Image.open('E:/test/dcms/ChengGuan/result/yzm.png')
        im2 = im.resize((1535, 863))
        rangle = (left, top, right, bottom)
        im3 = im2.crop(rangle)
        frame4 = im3.resize((90,30))
        frame4.save('E:/test/dcms/ChengGuan/result/yzm2.png')
        # filePath = "./result/yzm2.png"
        text = verificationCode(frame4)
        print(text)
        return text

if __name__=='__main__':
    driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")   
    url= getConstant.IP_WEB_91+'/dcms/bms/login.jsp'  
    test_login_authCode(driver,url)


