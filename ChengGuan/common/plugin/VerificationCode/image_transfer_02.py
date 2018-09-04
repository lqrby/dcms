import os
from PIL import Image
class pictureCleaning:
#清楚图片边框
    def removeFrame(self,img,width):
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

    #批量图片粗清理
    def image_transfer_arr(self,image_arry):
        """
        :param image_arry:图像list，每个元素为一副图像
        :return: image_clean:清理过后的图像list
        """
        image_clean = []
        threshold_grey = 100
        for i, image in enumerate(image_arry):
            self.removeFrame(image,width = 1)
            image = image.convert('L') # 转换为灰度图像，即RGB通道从3变为1
            im2 = Image.new("L", image.size, 255)
            for y in range(image.size[1]): # 遍历所有像素，将灰度超过阈值的像素转变为255（白）
                for x in range(image.size[0]):
                    pix = image.getpixel((x, y))
                    if int(pix) > threshold_grey:  # 灰度阈值
                        im2.putpixel((x, y), 255)
                    else:
                        im2.putpixel((x, y), pix)
            image_clean.append(im2)
        return image_clean

    #单个图片粗清理
    def image_transfer(self,image):
        """
        :param image:图片对象
        :return: imageClean:清理过后的图像对象
        """
        
        imageClean = []
        threshold_grey = 100
        image = image.convert('L') # 转换为灰度图像，即RGB通道从3变为1
        im2 = Image.new("L", image.size, 255)
        for y in range(image.size[1]): # 遍历所有像素，将灰度超过阈值的像素转变为255（白）
            for x in range(image.size[0]):
                pix = image.getpixel((x, y))
                if int(pix) > threshold_grey:  # 灰度阈值
                    im2.putpixel((x, y), 255)
                else:
                    im2.putpixel((x, y), pix)
        imageClean = self.removeFrame(im2,width = 1)
        return imageClean

