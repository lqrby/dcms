import requests,re
from common.constant_all import getConstant
from config.Log import logging

# 移动端案卷上报图片
def test_app_ReportPicture(imgUrl,picturePath):
    files = {'upload': ('image', open(picturePath,'rb'),'multipart/form-data')}
    objsbres = requests.post(url=imgUrl,files=files).text
    obj_result = re.compile("<issuc>(.*?)</issuc>").search(objsbres).group()
    if obj_result:
        print("案卷图片上传成功")
    else:
        print("XXXXXXXXXX执法局:案卷图片出现问题XXXXXXXXXX")

    