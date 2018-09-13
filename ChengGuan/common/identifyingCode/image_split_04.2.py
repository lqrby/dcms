import os , time
from PIL import Image
import pytesseract
#切割图片
# def image_split(image,outDir,count,p_w):

#     """
#     :param image:单幅图像

#     :return:单幅图像被切割后的图像list

#     """
    
#     w, h = image.size #图片宽高
#     pixdata = image.load()
#     # print("111111111111111111111111",pixdata)
#     # eachWidth = int(w / count) #计算图片平均宽度120/4 = 30
#     #########################################
#     inletter = False    #找出每个字母开始位置

#     foundletter = False #找出每个字母结束位置

#     start = 0

#     end = 0
#     #存储坐标

#     letters = []
#     # image = image.resize((180, 60)) #标准化图像格式
#     # image.show()

#     for x in range(image.size[0]):

#         for y in range(image.size[1]):

#             pix = image.getpixel((x, y))

#             if pix != True:

#                 inletter = True

#         if foundletter == False and inletter == True:

#             foundletter = True

#             start = x  #确定开始点

#     print("start = ",start)        
#     # eachWidth = int(( w - start * 2 ) / count) #计算图片平均宽度120/4 = 30
#     eachWidth = int(w / count) #计算图片平均宽度120/4 = 30
#     beforeX = 0
#     for i in range(count):
 
#         allBCount = []
#         nextXOri = (i + 1) * eachWidth
#         # X = 27~32 #w=120
#         for x in range(nextXOri - p_w, nextXOri + p_w): #从27开始，32循环结束 共循环6次
#             if x >= w: 
#                x = w - 1
#             if x < 0:
#                x = 0
#             b_count = 0
#            # 判断x的纵向坐标有多少白色像素
#             for y in range(h):
#                 # print("img的坐标是：",pixdata[x, y])
#                 if pixdata[x, y] == 0:
#                     b_count += 1 # 统计出现的白色像素的次数
#             #把每一次x坐标的列出现的空白总数以键值对的方式存入一个数字
#             allBCount.append({'x_pos': x, 'count':b_count}) 
#         # 对数组进行排序
#         sort = sorted(allBCount, key=lambda e: e.get('count'))
#         # 获取排序后第一组x值
#         nextX = sort[0]['x_pos']
        
#         box = (beforeX, 0, nextX, h) # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
#         time.sleep(2)
#         image.crop(box).save("F:/code/case/image/"+ outDir + str(i) + ".png")
#         letters.append(image.crop(box))  
#         time.sleep(2)
#         beforeX = nextX
#     return letters
            # if foundletter == True and inletter == False and x-start > 10:

            #     foundletter = False

            #     end = x

            #     letters.append((start, end))

            # inletter = False
    # print(letters)
 

    # 因为切割出来的图像有可能是噪声点

    # 筛选可能切割出来的噪声点,只保留开始结束位置差值最大的位置信息

    # 存储 结束-开始 值 
    
    ##############################
    # subtract_array = []
    # image_character_num = 4
    # for each in letters:

    #     subtract_array.append(each[1]-each[0])

    # reSet = sorted(subtract_array, key=lambda x:x, reverse=True)[0:image_character_num]

    # # 存储 最终选择的点坐标
    # letter_chioce = []

    # for each in letters:

    #     if int(each[1] - each[0]) in reSet:

    #         letter_chioce.append(each)

 
    # #存储切割后的图像
    # image_split_array = []
    # for letter in letter_chioce:

    #     im_split = image.crop((letter[0], 0, letter[1], image.size[1])) # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)

    #     # im_split = im_split.resize((image_width, image_height)) # 转换格式

    #     image_split_array.append(im_split)

 
    # return image_split_array[0:int(image_character_num)]


def smartSliceImg(img, outDir, count, p_w):
    '''
    :param img: 单幅图像
    :param outDir:切割后单幅图片的名称
    :param count: 切割多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    我们可以换种思想，在目标位置的前后进行垂直上的像素判断，判断某一列的黑色像素最少，就是切割点。
    '''
    w, h = img.size #图片宽高
    pixdata = img.load()
    eachWidth = int(w / count) #计算图片平均宽度120/4 = 30
    beforeX = 0
    for i in range(count):
 
        allBCount = []
        nextXOri = (i + 1) * eachWidth
        # X = 27~32 #w=120
        for x in range(nextXOri - p_w, nextXOri + p_w): #从27开始，32循环结束 共循环6次
            if x >= w: 
               x = w - 1
            if x < 0:
               x = 0
            b_count = 0
           # 判断x的纵向坐标有多少白色像素
            for y in range(h):
                print("img的坐标是：",pixdata[x, y])
                if pixdata[x, y] == 0:
                    b_count += 1 # 统计出现的白色像素的次数
            #把每一次x坐标的列出现的空白总数以键值对的方式存入一个数字
            allBCount.append({'x_pos': x, 'count':b_count}) 
        # 对数组进行排序
        sort = sorted(allBCount, key=lambda e: e.get('count'))
        # 获取排序后第一组x值
        nextX = sort[0]['x_pos']
        
        box = (beforeX, 0, nextX, h) # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
        
        img.crop(box).save("E:/code/python3CAPTCHA/img/"+ outDir + str(i) + ".png")
        beforeX = nextX
    return beforeX
        # text = pytesseract.image_to_string(beforeX)
        # print(nextX)
    # return beforeX

def image_split(img, outDir, count, p_w):
    '''
    :param img: 单幅图像
    :param outDir:切割后单幅图片的名称
    :param count: 切割多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    我们可以换种思想，在目标位置的前后进行垂直上的像素判断，判断某一列的黑色像素最少，就是切割点。
    '''
    w, h = img.size #图片宽高
    pixdata = img.load()
    inletter = False    #找出每个字母开始位置
    foundletter = False #找出每个字母结束位置
    start = 0
    end = 0
    letters = []    #存储坐标
    allBCount = []
    eachWidth = 14
    for x in range(img.size[0]): #循环图片的宽度  90
        # 循环黑白点 0 = 黑色 1 = 白色
        for y in range(img.size[1]):   #30

            pix = img.getpixel((x, y)) #图片的纵横坐标
            
            if pix != True: 

                inletter = True  #黑
        # 不是结束位置，并且黑色的标记为真条件成立
        if foundletter == False and inletter == True:
            
            start = x #裁剪开始位置17
            # 设置结束位置的条件为真
            foundletter = True
            # eachWidth = round((w - (start-1) * 2) / count) #计算图片平均宽度120/4 = 30  
            # print("5555555555555555555555555555555",eachWidth) #图片宽度14px
            # print("开始位置是：",start)
        if x > start + (eachWidth-p_w) and x < start + (eachWidth + p_w):  
            # print("满足条件一，x的值是：",x,"x - start = ",x - start,">",eachWidth-p_w)
            if foundletter == True and inletter == False:
                foundletter = False
                end = x
            # elif ( x - start) > (eachWidth + p_w):
            #     print("不满足条件，x的值是：",x)
            #     for x in range(w - p_w, w + p_w): #从27开始，32循环结束 共循环6次
            #         # if x >= w: 
            #         # x = w - 1
            #         # if x < 0:
            #         # x = 0
            #         b_count = 0
            #         # 判断x的纵向坐标有多少白色像素
            #         for y in range(h):
            #             # print("img的坐标是：",pixdata[x, y])
            #             if pixdata[x, y] == 0:
            #                 b_count += 1 # 统计出现的白色像素的次数
            #         #把每一次x坐标的列出现的空白总数以键值对的方式存入一个数字
            #         allBCount.append({'x_pos': x, 'count':b_count}) 
            #     # 对数组进行排序
            #         sort = sorted(allBCount, key=lambda e: e.get('count'))
            #     # 获取排序后第一组x值
            #     nextX = sort[0]['x_pos']
            #     end = nextX
            #     foundletter = False
                
            #     # box = (beforeX, 0, nextX, h) # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
            # print("end的值是：",end)
            # letters.append((start, end))
        inletter = False
    print(letters)
    # w, h = img.size #图片宽高
    # pixdata = img.load()
    # eachWidth = int(w / count) #计算图片平均宽度120/4 = 30
    # beforeX = 0
    # for i in range(count):
 
    #     allBCount = []
    #     nextXOri = (i + 1) * eachWidth  # 预计切割小图片的宽度
    #     # X = 27~32 #w=120

    #     for x in range(nextXOri - p_w, nextXOri + p_w): #从27开始，32循环结束 共循环6次
    #         if x >= w: 
    #            x = w - 1
    #         if x < 0:
    #            x = 0
    #         b_count = 0
    #        # 判断x的纵向坐标有多少白色像素
    #         for y in range(h):
    #             # print("img的坐标是：",pixdata[x, y])
    #             if pixdata[x, y] == 0:
    #                 b_count += 1 # 统计出现的白色像素的次数
    #         #把每一次x坐标的列出现的空白总数以键值对的方式存入一个数字
    #         allBCount.append({'x_pos': x, 'count':b_count}) 
    #     # 对数组进行排序
    #     sort = sorted(allBCount, key=lambda e: e.get('count'))
    #     # 获取排序后第一组x值
    #     nextX = sort[0]['x_pos']
        
    #     box = (beforeX, 0, nextX, h) # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
        
    #     img.crop(box)#.save("E:/code/python3CAPTCHA/img/"+ outDir + str(i) + ".png")
    #     split_imgs.append(img.crop(box))
    #     beforeX = nextX
    return letters


