import requests,re,time
from common.constant_all import getConstant
from config.Log import logging

# 移动端案卷上报图片
def test_app_ReportPicture(imgUrl,picturePath):
    app_header = {
        "User-Agent": "Android/8.0",
        "Connection":"Keep-Alive",
        "Accept-Encoding":"gzip"
    }
    for i,img in enumerate(picturePath):
        files = {'upload': ('image', open(img,'rb'),'multipart/form-data')}
        objsbres = requests.post(url=imgUrl,files=files,headers = app_header,timeout = 25)
        img_res = objsbres.text
        objsbres.connection.close()
        # time.sleep(1)
        # print(img_res)
        if 'true' in img_res:
            print("图片{0}上传成功".format(i+1))
        else:
            print("XXXXXXXXXX图片{0}出现问题XXXXXXXXXX".format(i+1))

    