# !/usr/bin/python3.4
# -*- coding: utf-8 -*-
from PIL import Image
import time

im = Image.open("yzm.png")
#(将图片转换为8位像素模式)
im = im.convert("P")
im2 = Image.new("P",im.size,255)
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        print(pix)
        if pix == 9 or pix == 3: # these are the numbers to get
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
count = 0
for letter in letters:
    # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    # im3.show()
    time.sleep(3)
    # 更改成用时间命名
    im3.save("./%s.gif" % (time.strftime('%Y%m%d%H%M%S', time.localtime())))
    count += 1
    print(count)







