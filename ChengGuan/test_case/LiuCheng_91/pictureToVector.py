from PIL import Image
# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

# if __name__ == "__main__":
#     im = Image.open('yzm1.gif')
#     im2 = buildvector(im)
#     print(im2)