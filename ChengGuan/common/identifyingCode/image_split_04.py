import os , time
from PIL import Image
import pytesseract
#切割图片
def image_split(img, outDir, count, p_w):
    '''
    :param img:
    :param outDir:
    :param count: 图片中有多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    '''
    inletter = False    #找出每个字母开始位置

    foundletter = False #找出每个字母结束位置

    w, h = img.size

    beforeX = 0

    letters = [] #存储坐标

    eachWidth = round( (w-28) / count)
    for i in range(count):
        
        # 1. 确定每一次切割的开始坐标
        inletter = False    #找出每个字母开始位置

        foundletter = False #找出每个字母结束位置

        # print("第{}次循环".format(i+1),beforeX,"----------",foundletter,inletter)
        #######################################
        for x in range(beforeX,w):  #循环宽度
            # print("x",x)
            for y in range(h): #循环高度

                pix = img.getpixel((x, y)) #坐标对象

                if pix != True: # 0 = false 1= true
                    # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",pix)
                    inletter = True  #黑色标记

                    # print("kaishi",foundletter)      
            # print("foundletter = ",foundletter,"-----------------inletter = ",inletter)
            #判断开始 第一个黑色为开始位置
            if foundletter == False and inletter == True:
                # 问题在这里，循环第二次开始没有进来
                foundletter = True
                
                beforeX = x  #开始位置

                # print("第",i+1,"次的开始坐标是：",beforeX)
                # print("我能循环多少次",x)
                #判断结束 第一个白色为结束
                # print("这里是开始的位置",beforeX)
                # break
                
            
        
        pixdata = img.load()
        
        # print("切割图片平均宽度",eachWidth)
        #######################################

        allBCount = []
        nextXOri = (i + 1) * eachWidth

        for xx in range(nextXOri +eachWidth - p_w, nextXOri +eachWidth + p_w):
            if xx >= w:
                xx = w - 1
            if xx < 0:
                xx = 0
            b_count = 0
            for yy in range(h):
                if pixdata[xx, yy] == 0:
                    b_count += 1
            allBCount.append({'x_pos': xx, 'count':b_count})
        sort = sorted(allBCount, key=lambda e: e.get('count'))

        nextX = sort[0]['x_pos']
        # print("第",i+1,"次的结束坐标是：",nextX)
        box = (beforeX, 0, nextX, h) # (切割的起始横坐标，起始纵坐标，切割结束的横坐标（宽度），切割的高度)
        # print("****",box)
        
        # inletter == False
        
        # time.sleep(2)
        # print(img.crop(box))
        # img.crop(box).save("F:/code/case/image/"+outDir+".png")
        img.crop(box).save("E:/test/dcms/ChengGuan/common/image/"+ outDir + str(i) + ".png")
        # time.sleep(2)
        letters.append(img.crop(box))
        beforeX = nextX
        # print("@@@@@第{}次循环结束@@@@".format(i+1))
    return letters

