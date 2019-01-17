import requests,re,time
from common.constant_all import getConstant
from config.Log import logging

# 移动端案卷上报图片
def test_app_ReportPicture(imgUrl,picturePath):
    for i,img in enumerate(picturePath):
        files = {'upload': ('image', open(img,'rb'),'multipart/form-data')}
        objsbres = requests.post(url=imgUrl,files=files,timeout = 15)
        objsbres.connection.close()
        time.sleep(1)
        if 'true' in objsbres.text:
            print("图片{0}上传成功".format(i+1))
        else:
            print("XXXXXXXXXX图片{0}出现问题XXXXXXXXXX".format(i+1))

    