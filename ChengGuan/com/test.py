from PIL import Image
from PIL import ImageEnhance
import pytesseract


# rangle = (1200,495,1280,525)
# i=Image.open("E:/test/dcms/ChengGuan/result/yzm.png") #打开截图
# frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
# frame4.save("E:/test/dcms/ChengGuan/com/img/yzm18.png")
#打开图片
im=Image.open('E:/test/dcms/ChengGuan/com/img/yzm18.png')
#图片二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

#PIL转换成黑白模式，将图片转换成简单的黑白两种颜色
im=im.convert('L') #转化成灰度
im = im.point(table,'1')
# imgResize = img_grey.resize((300,130)) #放大图片
imgSize = im.size
w,h = im.size
data = im
# data.show()
for x in range(1,w-1):
    if x > 1 and x != w-2:
        left = x - 1
        right = x + 1

    for y in range(1,h-1):
        up = y - 1
        down = y + 1

        if x <= 2 or x >= (w - 2):
            data.putpixel((x,y),255)

        elif y <= 2 or y >= (h - 2):
            data.putpixel((x,y),255)

        elif data.getpixel((x,y)) == 0:
            if y > 1 and y != h-1:
                up_color = data.getpixel((x,up))
                down_color = data.getpixel((x,down))
                left_color = data.getpixel((left,y))
                left_down_color = data.getpixel((left,down))
                right_color = data.getpixel((right,y))
                right_up_color = data.getpixel((right,up))
                right_down_color = data.getpixel((right,down))

                if down_color == 0:
                    if left_color == 255 and left_down_color == 255 and \
                        right_color == 255 and right_down_color == 255:
                        data.putpixel((x,y),255)
                        data.save("text2.png","png")

                elif right_color == 0:
                    if down_color == 255 and right_down_color == 255 and \
                        up_color == 255 and right_up_color == 255:
                        data.putpixel((x,y),255)
                        data.save("text3.png","png")

            if left_color == 255 and right_color == 255 \
                    and up_color == 255 and down_color == 255:
                data.putpixel((x,y),255)
        else:
            pass
data.save("yzm9.png","png")
im2=Image.open('yzm9.png')
im2.show()
print(pytesseract.image_to_string(im2))















