# coding:utf-8
from selenium import webdriver
from PIL import Image
import time,os


# coding:utf-8
from time import sleep
from PIL import Image
from selenium import webdriver
url='http://219.149.226.180:7897/dcms/bms/login.jsp'
driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
driver.maximize_window()  #将浏览器最大化  1535, 863
# driver.set_window_size(1024, 768)
driver.implicitly_wait(30)#隐式等待
driver.get(url)
sleep(2)
driver.save_screenshot('./result/yzm.png')  # 截取当前页面全图
element = driver.find_element_by_id("codeimg")  # 验证码标签对象
location = element.location
print("获取元素坐标：",location)
size = element.size
# 计算出元素上、下、左、右 位置
left = element.location['x']
top = element.location['y']+86
right = left + element.size['width']
bottom = top + element.size['height']

im = Image.open('./result/yzm.png')
print("jiu",im.size)
im2 = im.resize((1535, 863))
print("xin",im2.size)
print("left={}--top={}--right={}--bottom={}".format(left, top, right, bottom))
rangle = (left, top, right, bottom)
im3 = im2.crop(rangle)
# print(im3.size)
# im3.show()
im8 = im3.resize((90,30))
im8.save('./result/yzm2.png')
im8.show()
