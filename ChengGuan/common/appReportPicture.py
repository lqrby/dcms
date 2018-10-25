import requests,re
from common.constant_all import getConstant
from config.Log import logging

# 移动端案卷上报图片
def test_app_ReportPicture(imgUrl,picturePath):
    for i,img in enumerate(picturePath):
        files = {'upload': ('image', open(img,'rb'),'multipart/form-data')}
        objsbres = requests.post(url=imgUrl,files=files).text
        if '<issuc>' in objsbres:
            obj_result = re.compile("<issuc>(.*?)</issuc>").search(objsbres).group()
        else:
            obj_result = False
        if obj_result:
            print("图片%d上传成功"%i)
        else:
            print("XXXXXXXXXX图片%d出现问题XXXXXXXXXX"%i+1)

    