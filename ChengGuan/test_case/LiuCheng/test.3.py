# coding:utf-8
from selenium import webdriver
from PIL import Image
import time,os


 
infile = './result/yzm2.png'
outfile = './result/yzm3.png'
im = Image.open(infile)
# im.show()
(x,y) = im.size #read image size
x_s = 90 #define standard width
y_s = round(y * x_s / x) #calc height based on standard width
out = im.resize((x_s,y_s),Image.ANTIALIAS) #resize image with high-quality
out.show()
print("daxiao",out.size)
out.save(outfile)
 
print ('original size: ',x,y)
print ('adjust size: ',x_s,y_s)
 
'''
OUTPUT:
original size:  500 358
adjust size:  250 179
'''