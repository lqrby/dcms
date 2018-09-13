import os
from PIL import Image

#读取图片特征
def feature_transfer(image):
    """
    :param image （图像list）
    :return:feature （特征list）
    """
    image_width = 50
    image_height = 50
    image = image.resize((image_width, image_height)) #标准化图像格式
 
    feature = []#计算特征
    for x in range(image_width):#计算行特征
        feature_width = 0
        for y in range(image_height):
            if image.getpixel((x, y)) == 0:
                feature_width += 1
        feature.append(feature_width)
 
    for y in range(image_height): #计算列特征
        feature_height = 0
        for x in range(image_width):
            if image.getpixel((x, y)) == 0:
                feature_height += 1
        feature.append(feature_height)
    # print('feature length :',len(feature))
    print("feature vector:",feature)
    return feature