import os , time
from PIL import Image
import pytesseract
#切割图片
def image_split(image,outDir,count,p_w):
    '''
    :param img: 单幅图像
    :param outDir:切割后单幅图片的名称
    :param count: 切割多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    我们可以换种思想，在目标位置的前后进行垂直上的像素判断，判断某一列的黑色像素最少，就是切割点。
    '''

    inletter = False    #找出每个字母开始位置

    foundletter = False #找出每个字母结束位置

    start = 0

    end = 0

    letters = [] #存储坐标

    allBCount = []
    
    beforeX = 0

    # for i in range(count):
    for x in range(image.size[0]):  #循环宽度

        for y in range(image.size[1]): #循环高度

            pix = image.getpixel((x, y)) #坐标对象

            if pix != True: 

                inletter = True  #黑色标记

        #判断开始 第一个黑色为开始位置
        if foundletter == False and inletter == True:

            foundletter = True

            start = x  #开始位置

            #判断结束 第一个白色为结束
            print("start的值",start)
        # x = 
        if foundletter == True and inletter == False or (x > (start + 11) and start > 0) :
            b_count = 0
            foundletter = False
            #横向循环六次
            for j in range(start + 11,start + 17):
                # print("i的值：",i)
                #纵向循环图片的高度
                for z in range(image.size[1]):
                    pix2 = image.getpixel((j, z)) #坐标对象

                    if pix2 != False: 

                        b_count += 1 # 统计出现的白色像素的次数
                allBCount.append({'x_pos': j, 'count':b_count}) #次数组存放6次纵向白色像素出现的次数
            
            sort = sorted(allBCount, key=lambda e: e.get('count'))  # 6次统计完对数组进行排序挑出数量最大的x坐标

            end = sort[0]['x_pos']  # 获取排序后第一组x值
            box = (start, 0, end, image.size[1]) # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
            time.sleep(2)
            image.crop(box).save("F:/code/case/image/"+ outDir + ".png")
            letters.append(image.crop(box))  
            time.sleep(2)
            start = end
            print("end的值是：",end)
            # end = x
            # print("end的值是：",end)
            # letters.append((start, end))
            # print("start,end的值是：",start,end)
        inletter = False

    print(letters)

    
    return letters

