# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

# From:https://zhuanlan.zhihu.com/p/24222942
# 该知乎栏目为py2编写，这里改造成py3
import time
import os
from PIL import Image
from PIL import ImageEnhance
import sys
sys.path.append("E:/test/dcms/ChengGuan/common/plugin/VerificationCode")
# from read_captcha_01 import read_captcha
from image_transfer_02 import pictureCleaning
# from image_transfer_02 import image_transfer_arr,image_transfer
from image_Enhance_03 import image_Enhance
from image_split_04 import image_split
from image_split_04_test import smartSliceImg
from VectorCompare_05 import VectorCompare
from buildvector_06 import buildvector

def verificationCode(im):
    '''
    （1）读取图片，转换为灰度图像
    '''
    # filePath = 'E:/test/dcms/ChengGuan/common/img/174yzm.png'

    # im  = Image.open(filePath)
    # im.show()
    # im  = im.convert('L') # 转换为灰度图像，即RGB通道从3变为1
    '''
    （2）图像粗清理
        图像粗清理包括以下步骤：
        step 1：原始图像是RGB图像，即维度为 (26, 80, 3)。将其转换为灰度图像，维度变为(26, 80)。
        step 2：对于将要识别的验证码，显然，里面出现了很多用于干扰作用的灰色线条。博主通过设定灰度阈值（默认100），
        对图像中大于阈值的像素，赋值为255（灰度图像中像素值范围是0~255，其中255是白色，0是黑色）。
        发现对于此类型的验证码，这种方法很实用有木有。
    '''

    im2 = pictureCleaning().image_transfer(im)
    # im2.show()

    '''
    （3）图像细清理并二值化
        仅仅通过粗清理的办法，无法完全去除所有噪声点。此处引入了更细粒度的清理方法，参考这位大牛的清理方法。
        主要有3大步骤：
        step 1：找出图像中所有的孤立点；
        step 2：计算黑色点近邻9宫格中黑色点个数，若小于等于2个，那么认为该点为噪声点；
        step 3：去除所有噪声点。
        经过细清理后，虽然可以看到还存在一个噪声点，但效果其实很不错了。
    '''

    #对比度增强  

    image_contrasted = image_Enhance(im2)
    # image_contrasted.show()

    '''
    （4）单字符图像切割
        去除孤立点后，我们还是没法一下子就识别出这四个字符，需要对经过处理后的图片进行切分。（其实可以使用deep learning的方法进行识别，但本文仅介绍基于machine learning的识别方法）
        切割方式主要有一下步骤：
        step 1：找出图片中所有分离图像的开始结束位置。遍历width&height，当每出现一个黑色点，记为该字符开始位置；当新的一列出现全白色点，那么记为结束位置。
        [(8, 9), (14, 22), (29, 38), (42, 50), (57, 66)]
        step 2：尽管经过清理后，还是可能存在噪声点。在找到所有切割开始结束位置后，计算并选出（结束值-开始值）最大的切割位置。
        [(14, 22), (29, 38), (42, 50), (57, 66)]
    '''
    outDir = time.strftime("%Y%m%d%H%M%S", time.localtime())

    image_split_arr = image_split( image_contrasted, outDir , count = 4 , p_w = 3 ) 
    # image_split_arr = smartSliceImg( image_contrasted, outDir , count = 4 , p_w = 3 ) 

    #加载训练集，且把训练集也变成向量
    v = VectorCompare()
    
    iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    imageset = []

    for letter in iconset:

        for img in os.listdir('E:/test/dcms/ChengGuan/common/iconset/%s/' % (letter)):

            temp = []

            if img != "Thumbs.db" and img != ".DS_Store":

                temp.append(buildvector(Image.open("E:/test/dcms/ChengGuan/common/iconset/%s/%s" % (letter, img))))

            imageset.append({letter: temp})

    count = 0

    joinImgValue = []

    for im4 in image_split_arr:
        # print(im4)
        guess = []

        #将切割得到的验证码小片段与每个训练片段进行比较
        for image in imageset:
            
            for x,y in image.items():
                
                if len(y) != 0:

                    guess.append( ( v.relation(y[0],buildvector(im4)),x) )

        guess.sort(reverse=True)

        print("值：",guess[0])

        joinImgValue.append(guess[0][1])

        count += 1

        text = ''.join(joinImgValue)

        # print("验证码是：",text)

    return text,image_split_arr

# if __name__ == "__main__":
#     filePath = 'E:/test/dcms/ChengGuan/common/img/174yzm.png'
    # im  = Image.open(filePath)
#     verificationCode(im)