import os
from PIL import Image
from PIL import ImageEnhance,ImageFilter


def removeFrame(img, width):
    '''
    :param img:
    :param width: 边框的宽度
    :return:
    '''
    w, h = img.size
    pixdata = img.load()
    for x in range(width):
        for y in range(0, h):
            pixdata[x, y] = 255
    for x in range(w - width, w):
        for y in range(0, h):
            pixdata[x, y] = 255
    for x in range(0, w):
        for y in range(0, width):
            pixdata[x, y] = 255
    for x in range(0, w):
        for y in range(h - width, h):
            pixdata[x, y] = 255
    return img