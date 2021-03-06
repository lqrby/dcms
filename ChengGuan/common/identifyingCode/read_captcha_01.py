import os
from PIL import Image

#批量读取图片
def read_captcha(path):
    image_array = []
    image_label = []
    file_list = os.listdir(path)    # 获取captcha文件
    for file in file_list:
        image = Image.open(path + '/' + file)   # 打开图片
        file_name = file.split(".")[0]  #获取文件名，此为图片标签
        image_array.append(image)
        image_label.append(file_name)
    return image_array, image_label