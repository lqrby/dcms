from PIL import Image
from PIL import ImageEnhance
import pytesseract

#首先对PIL转换成黑白模式，将图片转换成简单的黑白两种颜色

# imgSize = img_grey.size

# print(imgSize)

# imgZisz.show()

#对比度增强  
# enh_con = ImageEnhance.Contrast(imgSize)  
# contrast = 1.5  
# image_contrasted = enh_con.enhance(contrast)  

# data = self.Im
# #图片的长宽
# w = self.w
# h = self.h
        
        #data.getpixel((x,y))获取目标像素点颜色。
        #data.putpixel((x,y),255)更改像素点颜色，255代表颜色。
        


# image_contrasted.show() 

# open
# from PIL import Image
# im = Image.open("1.png")
# im.show()
# format
# format属性定义了图像的格式，如果图像不是从文件打开的，那么该属性值为None；size属性是一个tuple，表示图像的宽和高（单位为像素）；mode属性为表示图像的模式，常用的模式为：L为灰度图，RGB为真彩色，CMYK为pre-press图像。如果文件不能打开，则抛出IOError异常。

# print(im.format, im.size, im.mode)
# save
# im.save("c:\\")
# convert()
# convert() 是图像实例对象的一个方法，接受一个 mode 参数，用以指定一种色彩模式，mode 的取值可以是如下几种： 
# · 1 (1-bit pixels, black and white, stored with one pixel per byte) 
# · L (8-bit pixels, black and white) 
# · P (8-bit pixels, mapped to any other mode using a colour palette) 
# · RGB (3x8-bit pixels, true colour) 
# · RGBA (4x8-bit pixels, true colour with transparency mask) 
# · CMYK (4x8-bit pixels, colour separation) 
# · YCbCr (3x8-bit pixels, colour video format) 
# · I (32-bit signed integer pixels) 
# · F (32-bit floating point pixels)

# im = Image.open('1.png').convert('L')
# Filter
# from PIL import Image, ImageFilter 
# im = Image.open(‘1.png’) 
# # 高斯模糊 
# im.filter(ImageFilter.GaussianBlur) 
# # 普通模糊 
# im.filter(ImageFilter.BLUR) 
# # 边缘增强 
# im.filter(ImageFilter.EDGE_ENHANCE) 
# # 找到边缘 
# im.filter(ImageFilter.FIND_EDGES) 
# # 浮雕 
# im.filter(ImageFilter.EMBOSS) 
# # 轮廓 
# im.filter(ImageFilter.CONTOUR) 
# # 锐化 
# im.filter(ImageFilter.SHARPEN) 
# # 平滑 
# im.filter(ImageFilter.SMOOTH) 
# # 细节 
# im.filter(ImageFilter.DETAIL) 

# 查看图像直方图

# im.histogram()

# 转换图像文件格式

# def img2jpg(imgFile):   
#      if type(imgFile)==str and imgFile.endswith(('.bmp', '.gif', '.png')):
#           with Image.open(imgFile) as im:
#               im.convert('RGB').save(imgFile[:-3]+'jpg')   
 

# 屏幕截图

# from PIL import ImageGrab 
# im = ImageGrab.grab((0,0,800,200)) #截取屏幕指定区域的图像 
# im = ImageGrab.grab() #不带参数表示全屏幕截图

# 图像裁剪与粘贴

# box = (120, 194, 220, 294) #定义裁剪区域 
# region = im.crop(box) #裁剪 
# region = region.transpose(Image.ROTATE_180) 
# im.paste(region,box) #粘贴

# 图像缩放

# im = im.resize((100,100)) #参数表示图像的新尺寸，分别表示宽度和高度

# #原始图像  
# image = Image.open('lena.jpg')  
# image.show()  

# #亮度增强  
# enh_bri = ImageEnhance.Brightness(image)  
# brightness = 1.5  
# image_brightened = enh_bri.enhance(brightness)  
# image_brightened.show()  

# #色度增强  
# enh_col = ImageEnhance.Color(image)  
# color = 1.5  
# image_colored = enh_col.enhance(color)  
# image_colored.show()  

# #对比度增强  
# enh_con = ImageEnhance.Contrast(image)  
# contrast = 1.5  
# image_contrasted = enh_con.enhance(contrast)  
# image_contrasted.show()  

# #锐度增强  
# enh_sha = ImageEnhance.Sharpness(image)  
# sharpness = 3.0  
# image_sharped = enh_sha.enhance(sharpness)  
# image_sharped.show()  
im=Image.open("E:/test/dcms/ChengGuan/result/2975yzm.png")
im=im.convert('L') #转化成灰度
# out = img_grey.point(table,'1')
im = im.resize((300,160)) #放大图片
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
img_out = im.point(table, '1')
img_out.show()

print(pytesseract.image_to_string(img_out))