# !/usr/bin/python3.4
# -*- coding: utf-8 -*-
import time
from PIL import Image
from PIL import ImageGrab
import unittest
import base64
import json
import requests
import os
import os.path
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import urllib
from selenium import webdriver
from config.Log import logging
from common.constant_all import getConstant
import pytesseract
from vectorValue import VectorCompare
from pictureToVector import buildvector

# url=getConstant.IP+'/dcms/bms/login.jsp'
# driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe") 
# driver.maximize_window()  #将浏览器最大化
# driver.implicitly_wait(100)#隐式等待
# driver.get(url)
# driver.save_screenshot('./result/yzm.png')  #截取当前网页，该网页有我们需要的验证码
# #rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
# rangle = (1200,495,1280,525)
# #rangle = (800,325,882,405)
# im=Image.open("./result/yzm.png") #打开截图
# im=im.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
# im.save("./result/yzm2.png")
im = Image.open("./result/yzm2.png")
# im.show()
#(将图片转换为8位像素模式)
im = im.convert("P")
im2 = Image.new("P",im.size,255)
#打印颜色直方图
#################################################################################################################
# his = im.histogram()
# print(his)
# values = {}
# for i in range(256):
#     values[i] = his[i]

# for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
#     print(j,k)
##################################################################################################################
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        # print(pix)
        if pix == 1: # these are the numbers to get
            im2.putpixel((y,x),0)

im2.show()
inletter = False
foundletter=False
start = 0
end = 0
letters = []
for y in range(im2.size[0]): 
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter=False
print(letters)
# count = 0
# for letter in letters:
#     # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
#     im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
#     # im3.show()
#     time.sleep(3)
#     # 更改成用时间命名
#     im3.save("./iconset/%s.png" % (time.strftime('%Y%m%d%H%M%S', time.localtime())))
#     count += 1
#     print(count)







