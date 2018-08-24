# -*- coding: utf-8 -*-
from PIL import Image
import unittest
import base64
import json
import requests
import os.path
import urllib
import time
import sys
import pytesseract
from selenium import webdriver
from PIL import Image
import time
from PIL import ImageGrab
sys.path.append("E:/test/dcms/ChengGuan")
from common.constant_all import getConstant

# path1=os.path.abspath('.')   # 表示当前所处的文件夹的绝对路径
# print(path1)

# print("地址是：" )
#     '''''接口名称：web_城管系统_获取验证码'''
def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    threshold = 140
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
 
    return table

def sum_9_region(img):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    x,y = img.size
    print(type(x),type(y))
    cur_pixel = img.getpixel((x,y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum


# driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")             
def test_login_authCode(driver):  #def test_jcjs_cl_post(self): 工单录入的方法
        url=getConstant.IP+'/dcms/bms/login.jsp'
        driver.maximize_window()  #将浏览器最大化
        driver.implicitly_wait(100)#隐式等待
        driver.get(url)
        driver.save_screenshot('E:/test/dcms/ChengGuan/com/img/yzm20.png')  #截取当前网页，该网页有我们需要的验证码
        rangle = (1200,495,1280,525)
        i=Image.open("E:/test/dcms/ChengGuan/com/img/yzm20.png") #打开截图
        nowImg=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
        #1.截取后保存为新的图片
        nowImg.save("E:/test/dcms/ChengGuan/com/img/yzm21.png")
        #2.PIL转换成黑白模式，将图片转换成简单的黑白两种颜色
        nowImg=nowImg.convert('L') #转化成灰度
        #3.图片二值化
        table = get_bin_table()
        img = nowImg.point(table,'1')
        #4.去除噪点
        sum_9_region(img)
        print(img.show())
        #图片文字识别        
        text = pytesseract.image_to_string(img)
        print("验证码是:",text)
        # 去掉识别结果中的特殊字符
        exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
        text = ''.join([x for x in text if x not in exclude_char_list])
        print("验证码是:",text)
        # return result

if __name__=='__main__':
        driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")  
        test_login_authCode(driver)


