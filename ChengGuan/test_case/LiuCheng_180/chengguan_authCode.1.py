# -*- coding: utf-8 -*-
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
import time
from selenium import webdriver
from config.Log import logging
from common.constant_all import getConstant
import pytesseract
from vectorValue import VectorCompare
from pictureToVector import buildvector
# From:https://zhuanlan.zhihu.com/p/24222942
# 该知乎栏目为py2编写，这里改造成py3
###########################################################################
#     '''''接口名称：web_城管系统_获取验证码'''
# driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")             
# def test_login_authCode(driver):  #def test_jcjs_cl_post(self): 工单录入的方法
#         url=getConstant.IP+'/dcms/bms/login.jsp'
#         driver.maximize_window()  #将浏览器最大化
#         driver.implicitly_wait(100)#隐式等待
#         driver.get(url)
#         driver.save_screenshot('./result/yzm.png')  #截取当前网页，该网页有我们需要的验证码
#         #rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
#         rangle = (1200,495,1280,525)
#         #rangle = (800,325,882,405)
#         i=Image.open("./result/yzm.png") #打开截图
#         frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
#         frame4.save("./result/yzm2.png")
        
#         print("验证码是：",result)
#         return result
###########################################################################
# url=getConstant.IP+'/dcms/bms/login.jsp'
# driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
# driver.maximize_window()  #将浏览器最大化
# driver.implicitly_wait(100)#隐式等待
# driver.get(url)
# driver.save_screenshot('./result/yzm.gif')  #截取当前网页，该网页有我们需要的验证码
# #rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
# rangle = (1200,495,1280,525)
# #rangle = (800,325,882,405)
# i=Image.open("./result/yzm.gif") #打开截图
# frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
# frame4.save("./result/yzm2.gif")
# #1.读取图片，打印图片的结构直方图
im = Image.open("./result/yzm2.gif")
im.show()
#打印颜色直方图
his = im.histogram()
print(his)
values = {}

for i in range(256):
    values[i] = his[i]

for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
    print(j,k)
#该数组长度为255，每一个元素代表（0-255）颜色的多少，例如最后一个元素为625，即255（代表的是白色）最多，组合在一起
# values = {}
# for i in range(0, 256):
#     values[i] = his[i]

# 排序，x:x[1]是按照括号内第二个字段进行排序,x:x[0]是按照第一个字段
# temp = sorted(values.items(), key=lambda x: x[1], reverse=True)
# print(temp)

# 占比最多的10种颜色
# for j, k in temp[:10]:
#     print(j, k)
#     255 625
#     212 365
#     220 186
#     219 135
#     169 132
#     227 116
#     213 115
#     234 21
#     205 18
#     184 15
#2.构造新的无杂质图片
#生成一张白底啥都没有的图片
# 获取图片大小，生成一张白底255的图片
im2 = Image.new("P", im.size, 255)
# (84, 22)
#原作者自己观察得到代表数字的颜色为220灰色和227红色
#将这些颜色根据宽和高的坐标以此写入新生成的白底照片中
# (84, 22)=(宽,高)=(size[0],size[1])
# 获得y坐标
# print(im.size)
for y in range(im.size[1]):
    # 获得y坐标
    for x in range(im.size[0]):
        # 获得坐标(x,y)的RGB值
        pix = im.getpixel((x, y))
        # print("*********************************************************************",pix)
        # 这些是要得到的数字
        if pix == 12 or pix == 15:
            # print("1111111111111111111111111111111111111111111111111111111111111111111")
            # 将黑色0填充到im2中
            im2.putpixel((x, y), 0)
# 生成了一张黑白二值照片
im2.show()

#3.切割图片
#x代表图片的宽，y代表图片的高
#对图片进行纵向切割
# 纵向切割
# 找到切割的起始和结束的横坐标
inletter = False #找出每个字母开始位置
foundletter = False #找出每个字母结束位置
start = 0
end = 0
letters = [] #存储坐标
for x in range(im2.size[0]):
    for y in range(im2.size[1]):
        pix = im2.getpixel((x, y))
        if pix != True:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = x

    if foundletter == True and inletter == False:
        foundletter = False
        end = x
        letters.append((start, end))
    inletter = False


    
print("坐标",letters)
# 打印结果为
# [(6, 14), (15, 25), (27, 35), (37, 46), (48, 56), (57, 67)]

#(6, 14)代表从x=6到x=14纵向切割成一条状

#保存字段到本地观察，这一步没有什么用，只是保存下来看看而已
# 保存切割下来的字段
# 可以看到保存下来的6个字段

# count = 0
# for letter in letters:
#     # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
#     im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
#     # im3.show()
#     time.sleep(3)
#     # 更改成用时间命名
#     im3.save("E:/test/dcms/ChengGuan/iconset/%s.gif" % (time.strftime('%Y%m%d%H%M%S', time.localtime())))
#     count += 1
#     print(count)

#4.训练识别
#使用的是 AI与向量空间图像识别
#将标准图片转换成向量坐标a，需要识别的图片字段为向量坐标b，cos(a,b)值越大说明夹角越小，越接近重合

#加载训练集，且把训练集也变成向量
v = VectorCompare() #创建对象
iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
imageset = []
for letter in iconset:
    # print(letter)
    for img in os.listdir('E:/test/dcms/ChengGuan/iconset/%s/' % (letter)):
        # print("88888888888888888888",img)
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("E:/test/dcms/ChengGuan/iconset/%s/%s" % (letter, img))))
        imageset.append({letter: temp})

#** 开始识别验证码 **
# 开始破解训练
count = 0
guess2 = []
for letter in letters:
    # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))

    guess = []
    

    # 将切割得到的验证码小片段与每个训练片段进行比较
    for image in imageset:
        # image.iteritems:报错'dict' object has no attribute 'iteritems'
        # 改成image.items()
        for x, y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0], buildvector(im3)), x))

            #x为iconset-x打印依次显示为0，1，2，3，。。。，x,y,z

            #排序选出夹角最小的（即cos值最大）的向量，夹角越小则越接近重合，匹配越接近
    guess.sort(reverse=True)
    guess2.append(guess[0][1])
    # print("验证码是：", guess[0][1])
    count += 1
    # print(guess2)
code = ''.join(guess2)
print("验证码是：",code)

# if __name__=='__main__':
#     test_login_authCode(driver)


