import os
from PIL import Image
from PIL import ImageEnhance,ImageFilter


def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
 
    return table

#图片细清除并二值化
def image_Enhance(image_clean):
    """
    :param image_clean:单幅图像
    :return:单幅图像被细清除并二值化后的图像
    """
    #对比度增强  
    enh_con = ImageEnhance.Contrast(image_clean)  
    contrast = 1.5  
    image_contrasted = enh_con.enhance(contrast)  
    # image_contrasted.show() 
    # 锐化 
    # image_contrasted.filter(ImageFilter.SHARPEN) 
    # # 平滑 
    # image_contrasted.filter(ImageFilter.SMOOTH) 
    # # 细节 
    # image_contrasted.filter(ImageFilter.DETAIL)
    # image_contrasted.show()

    table = get_bin_table()
    out = image_contrasted.point(table, '1')

    return out